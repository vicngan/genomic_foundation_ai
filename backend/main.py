import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

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
    """
    try:
        # Get OpenAI client (will be created on first use)
        openai_client = get_openai_client()
        
        # Convert messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        # Call vLLM server
        response = openai_client.chat.completions.create(
            model="qwen3",  # Model name as configured in vLLM
            messages=openai_messages,
            temperature=0.7,
            max_tokens=2048,
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
