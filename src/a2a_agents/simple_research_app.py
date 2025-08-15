"""
Simple Research Agent using Pydantic AI's built-in A2A support.
No FastA2A complexity - just clean, direct A2A protocol support.
"""

import os
import modal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Modal app for research agent
app = modal.App("simple-research-agent")

# Modal image with dependencies from root pyproject.toml + git support
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Required for GitPython and general git operations
    .pip_install_from_pyproject("pyproject.toml")  # Use root dependencies
)


@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    container_idle_timeout=300,
    timeout=60,
)
@modal.asgi_app()
def simple_research_agent():
    """Deploy Research Agent - Pydantic AI handles everything!"""
    from .research_agent import research_agent
    from .config import config
    
    config.setup_api_keys()
    
    # That's it! Pydantic AI's to_a2a() returns a complete ASGI app
    # with all A2A endpoints, docs, agent cards, etc.
    return research_agent.to_a2a()


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    from src.a2a_agents.research_agent import research_agent
    from src.a2a_agents.config import config
    
    print("🕵️‍♂️ Starting Research Agent locally on port 8002...")
    config.setup_api_keys()
    
    # Pydantic AI's to_a2a() returns a complete ASGI app - just run it!
    uvicorn.run(
        research_agent.to_a2a(),
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )
