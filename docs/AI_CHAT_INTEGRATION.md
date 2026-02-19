# Integrating the AI into the Chatbox

The chatbox is **already integrated** with the backend. Messages go: **Frontend → Backend → vLLM (AI)**. You only need to run the right services and set environment variables.

## Data flow

```
User types in chatbox
    → AIChatPanel sends POST to backend /chat
    → Backend injects system prompt and forwards to vLLM
    → vLLM (Qwen3 or other model) returns reply
    → Backend returns { reply } to frontend
    → Chatbox shows the AI response
```

No frontend code changes are required for basic integration.

---

## What you need to do

### 1. Run an LLM server (vLLM)

The backend talks to an **OpenAI-compatible** API. You can use:

**Option A: vLLM with Qwen3 (recommended in this project)**

- Run vLLM somewhere (e.g. Lighthouse HPC, or a machine with a GPU):
  ```bash
  # Example: run vLLM serving Qwen3 on port 8000
  python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000
  ```
- Note the URL. It must end with `/v1`, e.g. `http://<host>:8000/v1`.

**Option B: Any OpenAI-compatible API**

- e.g. LiteLLM, LocalAI, or a hosted API that supports the same chat completion format.
- Base URL must end with `/v1` if it follows the usual convention.

**Option C: OpenAI API**

- Use `https://api.openai.com/v1` and set `VLLM_API_KEY` to your OpenAI API key.  
- In `backend/config.py`, set `GenomicLLMConfig.MODEL_NAME` to the model you want (e.g. `gpt-4o-mini`).

### 2. Configure the backend

Point the backend at your LLM server.

**Environment variables (when starting the backend):**

```bash
# Required: URL of the LLM server (must include /v1)
export VLLM_SERVER_URL="http://YOUR_SERVER:8000/v1"

# If the API requires a key (e.g. OpenAI):
export VLLM_API_KEY="your-api-key"
# For vLLM without auth you can leave unset or use:
# VLLM_API_KEY=not-needed
```

Or create `backend/.env` (and load it, e.g. with `python-dotenv` or by sourcing it):

```env
VLLM_SERVER_URL=http://localhost:8000/v1
VLLM_API_KEY=not-needed
```

Replace `localhost:8000` with your vLLM host and port.

### 3. Start the backend

From the project root:

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be at `http://localhost:8000`. It will call the LLM using `VLLM_SERVER_URL`.

### 4. Configure the frontend

So the chatbox talks to your backend:

**Option A: Default (backend on same machine)**

- If the frontend runs on the same machine and the backend is at `http://localhost:8000`, you don’t need to set anything; the code defaults to `http://localhost:8000`.

**Option B: Backend on another host/port**

Create `.env` in the **project root** (next to `package.json`):

```env
VITE_API_BASE_URL=http://localhost:8000
```

Change to your backend URL, e.g. `http://192.168.1.10:8000`. Restart the frontend dev server after changing `.env`.

### 5. Start the frontend

```bash
# From project root
npm install
npm run dev
```

Open the app (e.g. `http://localhost:5173`). Use the chatbox; it will send requests to the backend, and the backend will use the AI.

---

## Quick checklist

| Step | Action |
|------|--------|
| 1 | vLLM (or other OpenAI-compatible server) is running and you know its URL (e.g. `http://host:8000/v1`). |
| 2 | `VLLM_SERVER_URL` (and optionally `VLLM_API_KEY`) set when starting the backend. |
| 3 | Backend started with `uvicorn main:app --reload` (e.g. on port 8000). |
| 4 | `VITE_API_BASE_URL` points to that backend (or leave default for localhost:8000). |
| 5 | Frontend started with `npm run dev` and you use the chat in the UI. |

---

## Troubleshooting

**Chatbox shows "Error: vLLM server not configured"**

- Backend could not create the OpenAI client. Check:
  - `VLLM_SERVER_URL` is set and has no typos.
  - URL ends with `/v1`.
  - No placeholder like `your-lighthouse-server` in the URL.

**"Error calling vLLM server" / timeouts**

- LLM server not reachable from the machine running the backend (firewall, wrong host/port).
- vLLM not running or crashed.
- Try: `curl -s http://YOUR_SERVER:8000/v1/models` (or your server’s health URL).

**Chatbox stays on "Thinking..." or never gets a reply**

- Backend might be waiting on the LLM. Check backend logs.
- Increase timeout in the frontend if the model is slow (see below).

**CORS errors in the browser**

- Backend already allows `http://localhost:5173` and `http://127.0.0.1:5173`. If you use another origin, add it to `CORSMiddleware` in `backend/main.py`.

---

## Optional: Improve robustness in the UI

- **Timeouts**: The frontend `fetch` has no timeout. For slow models, you can use `AbortController` with `setTimeout` and pass `signal` to `fetch`.
- **Retries**: Add a simple retry (e.g. 1–2 times) on network or 5xx errors before showing an error.
- **Status**: Call `GET /health` on load and show a “Backend connected” / “Backend unavailable” indicator so users know if the AI is reachable.

---

## Summary

- **Integration is already there:** the chatbox uses `POST /chat` and the backend uses the system prompt and forwards to vLLM.
- **You need to:** run an LLM server, set `VLLM_SERVER_URL` (and optionally `VLLM_API_KEY`), run the backend, set `VITE_API_BASE_URL` if needed, then run the frontend. After that, the AI is integrated into the chatbox.
