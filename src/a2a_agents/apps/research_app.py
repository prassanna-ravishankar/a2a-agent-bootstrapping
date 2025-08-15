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
app = modal.App("research-agent")

# Modal image with dependencies from root pyproject.toml + git support
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Required for GitPython dependency
    .env({"GIT_PYTHON_REFRESH": "quiet"})  # Suppress GitPython warnings
    .pip_install_from_pyproject("pyproject.toml")  # Use root dependencies
)


@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    scaledown_window=300,
    timeout=60,
)
@modal.asgi_app()
def research_agent_app():
    """Deploy Research Agent - Pydantic AI handles everything!"""
    from ..agents.research import research_agent
    from ..config import config
    
    config.setup_api_keys()
    
    # That's it! Pydantic AI's to_a2a() returns a complete ASGI app
    # with all A2A endpoints, docs, agent cards, etc.
    return research_agent.to_a2a()


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    from a2a_agents.agents.research import research_agent
    from a2a_agents.config import config
    
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
