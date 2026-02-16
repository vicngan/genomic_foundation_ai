from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat(payload: dict) -> dict:
    # Placeholder endpoint for future AI integration
    message = payload.get("message", "")
    return {
        "reply": (
            "This is a placeholder response from the backend. "
            "Integrate your AI provider here."
        ),
        "echo": message,
    }
