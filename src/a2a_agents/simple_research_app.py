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
    """Deploy Research Agent using Pydantic AI's native A2A support."""
    
    from .research_agent import research_agent
    from .config import config
    
    # Set up API key compatibility
    config.setup_api_keys()
    
    print("🕵️‍♂️ Initializing Research Agent with native A2A support...")
    print(f"🔧 Model: {config.MODEL_NAME}")
    
    # Use Pydantic AI's built-in A2A method - much simpler!
    app = research_agent.to_a2a()
    
    print("✅ Research Agent ready with native A2A protocol")
    return app


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    from src.a2a_agents.research_agent import research_agent
    from src.a2a_agents.config import config
    
    print("🕵️‍♂️ Starting Simple Research Agent locally...")
    print(f"🔧 Model: {config.MODEL_NAME}")
    print("📚 Native A2A Protocol: http://localhost:8002/")
    print("🌐 This uses Pydantic AI's built-in A2A support - no FastA2A!")
    
    # Set up API keys
    config.setup_api_keys()
    
    # Use the simple, native A2A method
    app = research_agent.to_a2a()
    
    print("✅ Research Agent initialized with native A2A")
    print("🎯 Ready for A2A communication")
    
    uvicorn.run(
        app,  # Direct ASGI app from to_a2a()
        host="0.0.0.0", 
        port=8002,
        reload=False,
        log_level="info"
    )
