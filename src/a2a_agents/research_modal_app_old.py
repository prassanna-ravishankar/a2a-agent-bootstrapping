"""
Standalone Modal app for the Research Agent.
Clean, simple deployment with A2A protocol support.
"""

import os
import modal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Modal app for research agent
app = modal.App("research-agent")

# Modal image with dependencies
image = modal.Image.debian_slim(python_version="3.11").pip_install([
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "pydantic-ai>=0.7.2",
    "fasta2a>=0.5.0",
    "duckduckgo-search>=6.3.5",
    "python-dotenv>=1.0.0",
    "httpx>=0.27.0",
])


@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    container_idle_timeout=300,
    timeout=60,
)
@modal.asgi_app()
def research_agent_app():
    """Deploy the Research Agent as a standalone A2A-compliant service."""
    
    from fastapi import FastAPI
    from .research_agent import research_agent
    from .config import config
    
    # Set up API key compatibility
    config.setup_api_keys()
    
    # Create the A2A app for this single agent
    research_a2a_app = research_agent.to_a2a(
        name="Research Agent",
        url="https://research-agent.modal.run",  # Will be updated with actual Modal URL
        version="1.0.0",
        description="Web search and information synthesis using DuckDuckGo API and Gemini 2.5 Flash Lite",
        provider={
            "name": "A2A Agent Bootstrapping",
            "url": "https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping",
        },
        skills=[
            {"name": "web_search", "description": "Search the web for information using DuckDuckGo"},
            {"name": "information_synthesis", "description": "Synthesize information from multiple sources"},
            {"name": "source_citation", "description": "Provide citations for information sources"},
            {"name": "fact_checking", "description": "Verify information against multiple sources"},
        ],
    )
    
    # Create main FastAPI app
    fastapi_app = FastAPI(
        title="Research Agent",
        description="AI-powered research agent with web search capabilities using Gemini 2.5 Flash Lite",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    
    # Health check endpoint
    @fastapi_app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "Research Agent",
            "version": "1.0.0",
            "model": "gemini-2.5-flash-lite",
            "capabilities": ["web_search", "information_synthesis", "source_citation"]
        }
    
    # Agent info endpoint
    @fastapi_app.get("/")
    async def agent_info():
        """Agent information and capabilities."""
        return {
            "name": "Research Agent",
            "description": "AI-powered research agent with web search capabilities",
            "model": "gemini-2.5-flash-lite",
            "capabilities": [
                "Web search using DuckDuckGo",
                "Information synthesis from multiple sources", 
                "Source citation and fact checking",
                "Real-time research queries"
            ],
            "endpoints": {
                "health": "/health",
                "docs": "/docs",
                "agent_card": "/.well-known/agent.json",
                "a2a_protocol": "/ (POST with A2A JSON-RPC)"
            }
        }
    
    # Set up proper lifespan for TaskManager
    @fastapi_app.on_event("startup")
    async def startup_event():
        """Initialize the A2A TaskManager."""
        await research_a2a_app.task_manager.__aenter__()
    
    @fastapi_app.on_event("shutdown") 
    async def shutdown_event():
        """Clean shutdown of A2A TaskManager."""
        await research_a2a_app.task_manager.__aexit__(None, None, None)
    
    # Mount the A2A app at root for A2A protocol compliance
    fastapi_app.mount("/", research_a2a_app)
    
    return fastapi_app


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    from src.a2a_agents.research_agent import research_agent
    from src.a2a_agents.config import config
    
    print("🕵️‍♂️ Starting Research Agent locally...")
    print(f"🔧 Model: {config.MODEL_NAME}")
    print("📚 API Documentation: http://localhost:8001/docs")
    print("🌐 A2A Protocol: http://localhost:8001/")
    
    # Set up API keys
    config.setup_api_keys()
    
    # Create the A2A app
    research_a2a_app = research_agent.to_a2a(
        name="Research Agent", 
        url="http://localhost:8001",
        version="1.0.0",
        description="Web search and information synthesis using DuckDuckGo API and Gemini 2.5 Flash Lite",
        provider={
            "name": "A2A Agent Bootstrapping",
            "url": "https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping",
        },
        skills=[
            {"name": "web_search", "description": "Search the web for information using DuckDuckGo"},
            {"name": "information_synthesis", "description": "Synthesize information from multiple sources"},
            {"name": "source_citation", "description": "Provide citations for information sources"},
        ],
    )
    
    # Create main FastAPI app
    from fastapi import FastAPI
    
    fastapi_app = FastAPI(
        title="Research Agent",
        description="AI-powered research agent with web search capabilities",
        version="1.0.0",
    )
    
    @fastapi_app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "Research Agent",
            "model": "gemini-2.5-flash-lite"
        }
    
    @fastapi_app.get("/")
    async def agent_info():
        return {
            "name": "Research Agent",
            "description": "AI-powered research agent with web search capabilities",
            "model": "gemini-2.5-flash-lite",
            "endpoints": {
                "health": "/health",
                "docs": "/docs", 
                "a2a_protocol": "/ (POST with A2A JSON-RPC)"
            }
        }
    
    # Set up proper lifespan for TaskManager
    @fastapi_app.on_event("startup")
    async def startup_event():
        """Initialize the A2A TaskManager."""
        await research_a2a_app.task_manager.__aenter__()
        print("✅ Research Agent TaskManager initialized")
    
    @fastapi_app.on_event("shutdown") 
    async def shutdown_event():
        """Clean shutdown of A2A TaskManager."""
        await research_a2a_app.task_manager.__aexit__(None, None, None)
        print("⏹️ Research Agent TaskManager shut down")
    
    # Mount A2A app
    fastapi_app.mount("/", research_a2a_app)
    
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )
