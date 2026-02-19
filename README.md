# Genomic Foundation Model (GFM) Platform

Welcome to the GFM Platform, an advanced web application designed for AI-powered genomic research. This platform provides a suite of tools for analyzing DNA sequences, managing research, and interacting with a specialized AI assistant trained specifically for genomic foundation model predictions.

## ✨ Features

The platform includes:

-   **Dashboard Overview**: A central hub to view your research activity, including total runs, confidence scores, recent results, and active jobs.
-   **New Analysis Runs**: Submit DNA sequences, FASTA files, or genomic regions for AI-powered predictions.
-   **Detailed Results**: View prediction scores, confidence assessments, and evidence panels with links to external databases like UCSC and Ensembl.
-   **Research Notebook**: A rich-text notebook to document research, embed result snapshots, and track version history for reproducibility.
-   **AI Assistant**: An integrated chat interface powered by Qwen3 (via vLLM) that helps explain results, compare analyses, answer questions about genomic research, and guide users through the prediction system. The AI is trained to reference only backend capabilities and prediction outputs.

## 🏛️ Architecture

This application uses a client-server architecture:

-   **Frontend**: A modern React single-page application (SPA) that provides the user interface.
-   **Backend**: A Python server built with FastAPI that integrates with vLLM (or other OpenAI-compatible APIs) to provide AI-powered chat assistance with genomic domain knowledge.
-   **AI Layer**: vLLM server running Qwen3 model (or compatible LLM) that processes chat requests with specialized genomic system prompts.

## 🛠️ Tech Stack

This project is built with a modern, robust technology stack:

-   **Frontend**:
    -   **Framework**: [React](https://reactjs.org/)
    -   **Language**: [TypeScript](https://www.typescriptlang.org/)
    -   **Styling**: [Tailwind CSS](https://tailwindcss.com/)
    -   **UI Components**: Custom components, likely using a library like [shadcn/ui](https://ui.shadcn.com/).
    -   **Routing**: [React Router](https://reactrouter.com/)
-   **Backend**:
    -   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
    -   **Language**: [Python](https://www.python.org/)
    -   **AI Integration**: OpenAI-compatible API (vLLM with Qwen3)
    -   **LLM**: Qwen3 model via vLLM for genomic domain-specific responses 

## 🚀 Getting Started

Follow these instructions to get a local copy up and running for development and testing purposes.

### Prerequisites

Make sure you have the following installed on your machine:

-   [Node.js](https://nodejs.org/) (v18 or newer recommended)
-   [npm](https://www.npmjs.com/), [yarn](https://yarnpkg.com/), or [pnpm](https://pnpm.io/)
-   [Python](https://www.python.org/downloads/) (v3.8 or newer recommended) & `pip`

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone <your-repository-url>
    cd genomic_model_ai
    ```

2.  **Set up the Backend:**
    Navigate to the backend directory, create a virtual environment, and install dependencies.
    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    The backend includes:
    - `/chat` endpoint with automatic system prompt injection
    - `/chat/with-template` endpoint for structured genomic queries
    - `/prompts/templates` endpoint to list available modalities
    - Genomic domain-specific prompt templates and configuration

3.  **Set up the Frontend:**
    From the root directory, install the Node.js dependencies.
    ```sh
    # In the root 'genomic_model_ai' directory
    npm install
    # or
    yarn install
    ```

4.  **Configure Environment Variables:**
    
    **Frontend** (create `.env` in project root):
    ```env
    VITE_API_BASE_URL=http://localhost:8000
    ```
    
    **Backend** (set environment variables or create `backend/.env`):
    ```env
    VLLM_SERVER_URL=http://your-vllm-server:8000/v1
    VLLM_API_KEY=not-needed 
    ```
    
    See `.env.example` for more details.


### Running the Application

You will need to run three services: the LLM server (vLLM), the backend, and the frontend.

**Prerequisites:** Ensure you have an LLM server running (vLLM with Qwen3 recommended). See [AI Chat Integration Guide](docs/AI_CHAT_INTEGRATION.md) for detailed setup.

1.  **Start the LLM Server (vLLM):**
    On your GPU server or local machine:
    ```sh
    python -m vllm.entrypoints.openai.api_server \
      --model Qwen/Qwen2.5-7B-Instruct \
      --port 8000
    ```
    Note the server URL (e.g., `http://localhost:8000/v1` or `http://your-server:8000/v1`).

2.  **Start the Backend Server:**
    From the `backend` directory (with the virtual environment activated):
    ```sh
    # Set the vLLM server URL
    export VLLM_SERVER_URL="http://your-vllm-server:8000/v1"
    export VLLM_API_KEY="not-needed"  # or your API key
    
    # Start the server
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    The backend API will be running at `http://localhost:8000`.

3.  **Start the Frontend Server:**
    From the root project directory:
    ```sh
    npm run dev
    ```
    The frontend will be running at `http://localhost:5173` (for Vite).

4.  **Access the Application:**
    Open `http://localhost:5173` in your browser. The AI chat assistant will be available in the chat panel.

**Note:** For detailed AI integration instructions, troubleshooting, and alternative LLM setups, see [docs/AI_CHAT_INTEGRATION.md](docs/AI_CHAT_INTEGRATION.md).



## 📁 Project Structure

```
genomic_model_ai/
├── src/                          # Frontend React application
│   ├── components/               # Reusable React components
│   │   └── layout/
│   │       └── AIChatPanel.tsx   # AI chat interface
│   └── ...
├── backend/                       # Backend FastAPI application
│   ├── main.py                   # Main API server with chat endpoints
│   ├── config.py                 # Genomic LLM configuration & system prompts
│   ├── prompt_templates.py       # Prompt templates for genomic queries
│   ├── requirements.txt          # Python dependencies
│   └── training/                 # LLM training infrastructure
│       ├── training_data.jsonl   # Training examples (18 examples)
│       ├── TRAINING_DATA.md      # Training documentation
│       ├── data_preparation.py   # Data prep scripts
│       ├── fine_tune_config.py  # Fine-tuning configuration
│       └── evaluation.py         # Evaluation metrics
├── docs/                          # Documentation
│   └── AI_CHAT_INTEGRATION.md   # AI integration guide
├── .env.example                  # Environment variable template
└── README.md                     # This file
```

### Key Backend Files

- **`backend/main.py`**: FastAPI server with `/chat`, `/chat/with-template`, and `/prompts/templates` endpoints
- **`backend/config.py`**: System prompt and genomic domain configuration
- **`backend/prompt_templates.py`**: Structured query templates for EFP, GEP, and EAP tasks
- **`backend/training/training_data.jsonl`**: 18 training examples for fine-tuning the LLM

## 📚 Documentation

- **[AI Chat Integration Guide](docs/AI_CHAT_INTEGRATION.md)**: Complete guide for setting up and integrating the AI chat assistant
- **[Training Data Documentation](backend/training/TRAINING_DATA.md)**: Training examples and system capabilities reference

## 🔧 API Endpoints

### Chat Endpoints

- **`POST /chat`**: Standard chat endpoint with automatic system prompt injection
  - Request: `{ "messages": [{"role": "user", "content": "..."}] }`
  - Response: `{ "reply": "..." }`

- **`POST /chat/with-template`**: Structured genomic query endpoint
  - Request: `{ "task_type": "EFP", "chromosome": "1", "start": 1000000, "end": 1600000, "cell_type": "HeLa", ... }`
  - Validates inputs and formats queries using genomic templates

- **`GET /prompts/templates`**: List available task types and modalities

- **`GET /health`**: Health check endpoint

## 🎯 AI Features

The AI assistant is configured to:
- Only reference backend system capabilities (no external knowledge)
- Explain genomic prediction results (EFP, GEP, EAP)
- Guide users through query formatting
- Interpret scores, confidence levels, and classifications
- Compare results from different modalities
- Provide system-specific guidance

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improving the platform, please feel free to open an issue or submit a pull request.

## 📄 License

This project is proprietary. All rights reserved. (Or specify an open-source license like MIT if applicable).
