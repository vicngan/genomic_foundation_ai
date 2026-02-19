import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
try:
    from .config import GenomicLLMConfig
    from .prompt_templates import get_template_for_task
except ImportError:
    # Fallback for direct execution
    from config import GenomicLLMConfig
    from prompt_templates import get_template_for_task

app = FastAPI(title="GFM Backend")

# Allow local frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration for vLLM (OpenAI-compatible API)
VLLM_SERVER_URL = os.getenv("VLLM_SERVER_URL", "http://localhost:8000/v1")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "not-needed")  # vLLM doesn't require auth by default

# Lazy initialization - client will be created on first use
_openai_client: Optional[OpenAI] = None


def get_openai_client() -> OpenAI:
    """
    Get or create the OpenAI client for vLLM.
    Validates the URL before creating the client.
    """
    global _openai_client
    
    if _openai_client is None:
        # Validate URL format
        if not VLLM_SERVER_URL or "your-lighthouse-server" in VLLM_SERVER_URL or ":port" in VLLM_SERVER_URL:
            raise ValueError(
                f"Invalid VLLM_SERVER_URL: {VLLM_SERVER_URL}. "
                "Please set VLLM_SERVER_URL to a valid URL (e.g., http://your-server:8000/v1)"
            )
        
        try:
            _openai_client = OpenAI(
                base_url=VLLM_SERVER_URL,
                api_key=VLLM_API_KEY,
            )
        except Exception as e:
            raise ValueError(
                f"Failed to initialize OpenAI client with URL {VLLM_SERVER_URL}: {str(e)}"
            )
    
    return _openai_client


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that forwards messages to vLLM server with Qwen3 model.
    Expects messages in OpenAI chat format.
    Automatically injects system prompt if not present.
    """
    try:
        # Get OpenAI client (will be created on first use)
        openai_client = get_openai_client()
        
        # Convert messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Check if system message already exists
        has_system_message = any(
            msg.get("role") == "system" 
            for msg in openai_messages
        )
        
        # Inject system prompt if not present
        if not has_system_message:
            system_prompt = GenomicLLMConfig.get_system_prompt()
            openai_messages.insert(0, {
                "role": "system",
                "content": system_prompt
            })

        # Call vLLM server
        response = openai_client.chat.completions.create(
            model=GenomicLLMConfig.MODEL_NAME,
            messages=openai_messages,
            temperature=GenomicLLMConfig.DEFAULT_TEMPERATURE,
            max_tokens=GenomicLLMConfig.DEFAULT_MAX_TOKENS,
        )

        reply = response.choices[0].message.content

        return ChatResponse(reply=reply)

    except ValueError as e:
        # Configuration error
        raise HTTPException(
            status_code=503,
            detail=f"vLLM server not configured: {str(e)}"
        )
    except Exception as e:
        # API call error
        raise HTTPException(
            status_code=500,
            detail=f"Error calling vLLM server: {str(e)}"
        )


class TemplateRequest(BaseModel):
    task_type: str
    chromosome: str
    start: int
    end: int
    cell_type: str
    modalities: Optional[List[str]] = None
    atac_seq_path: Optional[str] = None
    user_message: Optional[str] = None


class TemplateResponse(BaseModel):
    query: str
    task_type: str


@app.post("/chat/with-template", response_model=ChatResponse)
async def chat_with_template(template_request: TemplateRequest) -> ChatResponse:
    """
    Chat endpoint with automatic template formatting for genomic queries.
    Generates a formatted query and sends it to the LLM.
    """
    try:
        # Validate chromosome
        if not GenomicLLMConfig.validate_chromosome(template_request.chromosome):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid chromosome: {template_request.chromosome}. Valid chromosomes are: {GenomicLLMConfig.VALID_CHROMOSOMES}"
            )
        
        # Validate region size
        if not GenomicLLMConfig.validate_region_size(template_request.start, template_request.end):
            raise HTTPException(
                status_code=400,
                detail=f"Region size exceeds maximum of {GenomicLLMConfig.MAX_REGION_SIZE_KB}kb"
            )
        
        # Get appropriate template
        template = get_template_for_task(template_request.task_type)
        
        # Format query based on task type
        if template_request.task_type.upper() == "EFP":
            query = template.format_efp_query(
                chromosome=template_request.chromosome,
                start=template_request.start,
                end=template_request.end,
                cell_type=template_request.cell_type,
                include_additional_tfs="Additional TF-bindings" in (template_request.modalities or []),
                atac_seq_path=template_request.atac_seq_path
            )
        elif template_request.task_type.upper() == "GEP":
            query = template.format_gep_query(
                chromosome=template_request.chromosome,
                start=template_request.start,
                end=template_request.end,
                cell_type=template_request.cell_type,
                expression_modalities=template_request.modalities,
                atac_seq_path=template_request.atac_seq_path
            )
        elif template_request.task_type.upper() == "EAP":
            query = template.format_eap_query(
                chromosome=template_request.chromosome,
                start=template_request.start,
                end=template_request.end,
                cell_type=template_request.cell_type,
                include_starr_seq="STARR-seq" in (template_request.modalities or []),
                include_chromatin=any(m in (template_request.modalities or []) for m in ["Hi-C", "Micro-C"]),
                atac_seq_path=template_request.atac_seq_path
            )
        else:
            # Use generic template
            query = template.format_query(
                chromosome=template_request.chromosome,
                start=template_request.start,
                end=template_request.end,
                modalities=template_request.modalities or [],
                cell_type=template_request.cell_type,
                atac_seq_path=template_request.atac_seq_path
            )
        
        # Prepare messages with system prompt
        openai_client = get_openai_client()
        system_prompt = GenomicLLMConfig.get_system_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": template_request.user_message or f"Generate a prediction query for:\n\n{query}"}
        ]
        
        # Call vLLM server
        response = openai_client.chat.completions.create(
            model=GenomicLLMConfig.MODEL_NAME,
            messages=messages,
            temperature=GenomicLLMConfig.DEFAULT_TEMPERATURE,
            max_tokens=GenomicLLMConfig.DEFAULT_MAX_TOKENS,
        )
        
        reply = response.choices[0].message.content
        return ChatResponse(reply=reply)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing template request: {str(e)}"
        )


@app.get("/prompts/templates")
async def list_templates() -> dict:
    """
    List available prompt templates and modalities.
    """
    return {
        "task_types": GenomicLLMConfig.TASK_TYPES,
        "modalities": GenomicLLMConfig.MODALITIES,
        "constraints": {
            "max_region_size_kb": GenomicLLMConfig.MAX_REGION_SIZE_KB,
            "valid_chromosomes": GenomicLLMConfig.VALID_CHROMOSOMES,
        }
    }
