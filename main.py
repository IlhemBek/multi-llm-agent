from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import run_agent

app = FastAPI(
    title="Multi-LLM AI Agent API",
    description="An AI agent powered by Claude or Groq with weather, calculator, and web search tools.",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    query: str
    provider: Optional[str] = "claude"  # "claude" or "groq"
    model: Optional[str] = None


class QueryResponse(BaseModel):
    success: bool
    provider: str
    query: str
    response: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
def root():
    return {
        "message": "Multi-LLM AI Agent is running!",
        "docs": "/docs",
        "providers": ["claude", "groq"],
        "tools": ["get_weather", "calculate", "web_search"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    if request.provider not in ["claude", "groq"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid provider. Choose 'claude' or 'groq'."
        )
    
    result = run_agent(
        query=request.query,
        provider=request.provider,
        model=request.model
    )
    
    return QueryResponse(**result)
