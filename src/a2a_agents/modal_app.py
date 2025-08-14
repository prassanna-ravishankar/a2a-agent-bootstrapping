"""Main FastAPI application for A2A Agent Bootstrapping deployment on Modal.com."""

import os
from contextlib import asynccontextmanager

import modal
from pydantic_ai.models import KnownModelName
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# Import A2A applications (Pydantic AI native approach)
from .a2a_apps import (
    research_a2a_app,
    code_a2a_app, 
    data_a2a_app,
    planning_a2a_app,
)

# Define the Modal image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Required for GitPython in code_agent
    .pip_install_from_pyproject("pyproject.toml")
)

# Create Modal app
app = modal.App(
    "a2a-agent-bootstrapping", 
    image=image,
    secrets=[modal.Secret.from_name("gemini-api-key", required_keys=["GEMINI_API_KEY"])]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 A2A Agent Bootstrapping starting up...")
    print("🔧 Initializing agents...")
    
    # Set GitPython environment variable to quiet refresh messages
    os.environ.setdefault("GIT_PYTHON_REFRESH", "quiet")
    
    # Validate environment variables
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("⚠️  Warning: GEMINI_API_KEY not found in environment")
    else:
        print("✅ Gemini API key configured")
    
    print("🎯 All agents ready for A2A communication")
    yield
    # Shutdown
    print("⏹️ A2A Agent Bootstrapping shutting down...")


# Create FastAPI application
fastapi_app = FastAPI(
    title="A2A Agent Bootstrapping",
    description="""
    A showcase of four specialized, highly capable, and application-agnostic agents
    built using the A2A protocol. This foundational project demonstrates scalable
    and modular multi-agent systems.

    ## Agents Available

    ### 🕵️‍♂️ Research Agent
    Answers complex queries by searching the web and synthesizing information.

    ### 💻 Code Agent  
    Generates new code or reviews code from GitHub repositories.

    ### 🔄 Data Transformation Agent
    Cleans and structures raw, messy data into specified formats.

    ### 🧠 Logic and Planning Agent
    Breaks down high-level goals into logical, sequential plans of actionable steps.

    ## Core Technologies
    - **Agent Framework**: pydantic-ai for A2A communication
    - **Web Framework**: FastAPI for creating the web service  
    - **Hosting**: modal.com for serverless deployment
    - **LLM**: Gemini (free tier) as the reasoning engine
    - **External Tools**: DuckDuckGo API, GitPython
    """,
    version="0.1.0",
    contact={
        "name": "Prass, The Nomadic Coder",
        "email": "contact@a2aregistry.org",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping/blob/main/LICENSE",
    },
    lifespan=lifespan,
)

# Add CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi_app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with HTML interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>A2A Agent Bootstrapping</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px; margin: 0 auto; padding: 2rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; min-height: 100vh;
            }
            .container { 
                background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
                padding: 2rem; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            h1 { text-align: center; font-size: 3rem; margin-bottom: 1rem; }
            .subtitle { text-align: center; font-size: 1.2rem; margin-bottom: 3rem; opacity: 0.9; }
            .agents { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
            .agent { 
                background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px;
                border: 1px solid rgba(255,255,255,0.2); transition: transform 0.3s ease;
            }
            .agent:hover { transform: translateY(-5px); }
            .agent-title { font-size: 1.3rem; font-weight: bold; margin-bottom: 0.5rem; }
            .agent-desc { opacity: 0.9; margin-bottom: 1rem; }
            .links { text-align: center; margin-top: 3rem; }
            .links a { 
                color: white; text-decoration: none; margin: 0 1rem; 
                padding: 0.7rem 1.5rem; background: rgba(255,255,255,0.2);
                border-radius: 10px; transition: all 0.3s ease;
            }
            .links a:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 A2A Agent Bootstrapping</h1>
            <p class="subtitle">Four specialized agents showcasing scalable multi-agent systems</p>
            
            <div class="agents">
                <div class="agent">
                    <div class="agent-title">🕵️‍♂️ Research Agent</div>
                    <div class="agent-desc">
                        Answers complex queries by searching the web and synthesizing information from multiple sources.
                    </div>
                    <strong>A2A Endpoint:</strong> <code>/research/*</code>
                </div>
                
                <div class="agent">
                    <div class="agent-title">💻 Code Agent</div>
                    <div class="agent-desc">
                        Generates new code from descriptions or reviews existing code from GitHub repositories.
                    </div>
                    <strong>A2A Endpoint:</strong> <code>/code/*</code>
                </div>
                
                <div class="agent">
                    <div class="agent-title">🔄 Data Transformation Agent</div>
                    <div class="agent-desc">
                        Cleans and structures raw, messy data into well-organized formats like JSON, CSV, XML.
                    </div>
                    <strong>A2A Endpoint:</strong> <code>/data/*</code>
                </div>
                
                <div class="agent">
                    <div class="agent-title">🧠 Logic and Planning Agent</div>
                    <div class="agent-desc">
                        Breaks down high-level goals into logical, sequential plans of actionable steps.
                    </div>
                    <strong>A2A Endpoint:</strong> <code>/planning/*</code>
                </div>
            </div>
            
            <div class="links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/health">🔍 Health Check</a>
                <a href="/agents">🤖 Agent List</a>
                <a href="https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping">⭐ GitHub</a>
            </div>
            
            <div style="margin-top: 2rem; text-align: center; opacity: 0.8; font-size: 0.9rem;">
                <p><strong>🚀 Native A2A Protocol Implementation</strong></p>
                <p>All agents exposed via Pydantic AI's built-in A2A protocol compliance</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@fastapi_app.get("/health")
async def health_check():
    """Global health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "A2A Agent Bootstrapping",
            "version": "0.1.0",
            "protocol": "A2A (Agent-to-Agent)",
            "agents": {
                "research": "🕵️‍♂️ Research Agent - /research/*",
                "code": "💻 Code Agent - /code/*", 
                "data": "🔄 Data Transformation Agent - /data/*",
                "planning": "🧠 Logic and Planning Agent - /planning/*"
            },
            "endpoints": {
                "docs": "/docs - API Documentation",
                "health": "/health - This health check",
                "agents": "/agents - List all agents"
            }
        }
    )


@fastapi_app.get("/agents")
async def list_agents():
    """List all available agents and their capabilities."""
    return JSONResponse(
        content={
            "total_agents": 4,
            "agents": [
                {
                    "name": "Research Agent",
                    "emoji": "🕵️‍♂️",
                    "prefix": "/research",
                    "description": "Web search and information synthesis",
                    "protocol": "A2A via Pydantic AI",
                    "capabilities": ["web_search", "information_synthesis", "source_citation"]
                },
                {
                    "name": "Code Agent", 
                    "emoji": "💻",
                    "prefix": "/code",
                    "description": "Code generation and GitHub repository review",
                    "protocol": "A2A via Pydantic AI",
                    "capabilities": ["code_generation", "repository_analysis", "issue_detection"]
                },
                {
                    "name": "Data Transformation Agent",
                    "emoji": "🔄", 
                    "prefix": "/data",
                    "description": "Data cleaning and format transformation",
                    "protocol": "A2A via Pydantic AI",
                    "capabilities": ["data_parsing", "format_conversion", "data_cleaning"]
                },
                {
                    "name": "Logic and Planning Agent",
                    "emoji": "🧠",
                    "prefix": "/planning", 
                    "description": "Goal breakdown and strategic planning",
                    "protocol": "A2A via Pydantic AI", 
                    "capabilities": ["goal_analysis", "task_decomposition", "strategic_planning"]
                }
            ]
        }
    )


# Mount A2A applications (Pydantic AI's native approach)
fastapi_app.mount("/research", research_a2a_app, name="research_agent")
fastapi_app.mount("/code", code_a2a_app, name="code_agent")
fastapi_app.mount("/data", data_a2a_app, name="data_agent") 
fastapi_app.mount("/planning", planning_a2a_app, name="planning_agent")


# Deploy on Modal
@app.function()
@modal.asgi_app()
def fastapi_app_modal():
    """Deploy the FastAPI app on Modal."""
    return fastapi_app


if __name__ == "__main__":
    # For local development
    import uvicorn
    
    print("🚀 Starting A2A Agent Bootstrapping locally...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🌐 Web Interface: http://localhost:8000/")
    
    uvicorn.run(
        "a2a_agents.modal_app:fastapi_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
