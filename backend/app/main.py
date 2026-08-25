from fastapi import FastAPI

app = FastAPI(
    title="CloudTask AI API",
    description="AI-powered cloud task management platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "cloudtask-ai-api",
        "version": "0.1.0",
    }
