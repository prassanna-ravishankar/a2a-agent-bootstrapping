"""Main FastAPI application for A2A Agent Bootstrapping deployment on Modal.com."""

import os
from contextlib import asynccontextmanager

import modal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# Import all agent routers
from src.a2a_agents.code_agent_router import code_router
from src.a2a_agents.data_transformation_router import data_transformation_router
from src.a2a_agents.planning_agent_router import planning_router
from src.a2a_agents.research_agent_router import research_router

# Define the Modal image with all dependencies
image = modal.Image.debian_slim(python_version="3.11").pip_install_from_pyproject_toml("pyproject.toml")

# Create Modal app
app_modal = modal.App("a2a-agent-bootstrapping", image=image)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 A2A Agent Bootstrapping starting up...")
    print("🔧 Initializing agents...")
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
                    <strong>Endpoint:</strong> <code>/research/query</code>
                </div>
                
                <div class="agent">
                    <div class="agent-title">💻 Code Agent</div>
                    <div class="agent-desc">
                        Generates new code from descriptions or reviews existing code from GitHub repositories.
                    </div>
                    <strong>Endpoints:</strong> <code>/code/generate</code>, <code>/code/review</code>
                </div>
                
                <div class="agent">
                    <div class="agent-title">🔄 Data Transformation Agent</div>
                    <div class="agent-desc">
                        Cleans and structures raw, messy data into well-organized formats like JSON, CSV, XML.
                    </div>
                    <strong>Endpoint:</strong> <code>/data/transform</code>
                </div>
                
                <div class="agent">
                    <div class="agent-title">🧠 Logic and Planning Agent</div>
                    <div class="agent-desc">
                        Breaks down high-level goals into logical, sequential plans of actionable steps.
                    </div>
                    <strong>Endpoint:</strong> <code>/planning/plan</code>
                </div>
            </div>
            
            <div class="links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/health">🔍 Health Check</a>
                <a href="https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping">⭐ GitHub</a>
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
            "agents": {
                "research": "🕵️‍♂️ Research Agent - /research/*",
                "code": "💻 Code Agent - /code/*", 
                "data": "🔄 Data Transformation Agent - /data/*",
                "planning": "🧠 Logic and Planning Agent - /planning/*"
            },
            "endpoints": {
                "docs": "/docs - API Documentation",
                "redoc": "/redoc - Alternative API Docs",
                "health": "/health - This health check"
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
                    "key_endpoints": ["/research/query", "/research/health", "/research/info"]
                },
                {
                    "name": "Code Agent", 
                    "emoji": "💻",
                    "prefix": "/code",
                    "description": "Code generation and GitHub repository review",
                    "key_endpoints": ["/code/generate", "/code/review", "/code/health", "/code/info"]
                },
                {
                    "name": "Data Transformation Agent",
                    "emoji": "🔄", 
                    "prefix": "/data",
                    "description": "Data cleaning and format transformation",
                    "key_endpoints": ["/data/transform", "/data/formats", "/data/health", "/data/info"]
                },
                {
                    "name": "Logic and Planning Agent",
                    "emoji": "🧠",
                    "prefix": "/planning", 
                    "description": "Goal breakdown and strategic planning",
                    "key_endpoints": ["/planning/plan", "/planning/analyze", "/planning/health", "/planning/info"]
                }
            ]
        }
    )


# Include all agent routers with their prefixes
fastapi_app.include_router(research_router)
fastapi_app.include_router(code_router)
fastapi_app.include_router(data_transformation_router)
fastapi_app.include_router(planning_router)


# Deploy on Modal
@app_modal.asgi_app()
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
        "modal_app:fastapi_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
