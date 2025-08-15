"""
Simple Planning Agent using Pydantic AI's built-in A2A support.
"""

import os
import modal
from dotenv import load_dotenv

load_dotenv()

app = modal.App("planning-agent")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Required for GitPython dependency
    .env({"GIT_PYTHON_REFRESH": "quiet"})  # Suppress GitPython warnings
    .pip_install_from_pyproject("pyproject.toml")
)

@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    scaledown_window=300,
    timeout=60,
)
@modal.asgi_app()
def planning_agent_app():
    """Deploy Planning Agent - Pydantic AI handles everything!"""
    from ..agents.planning import planning_agent
    from ..config import config
    
    config.setup_api_keys()
    return planning_agent.to_a2a()

if __name__ == "__main__":
    import uvicorn
    from a2a_agents.agents.planning import planning_agent
    from a2a_agents.config import config
    
    print("🧠 Starting Planning Agent locally on port 8005...")
    config.setup_api_keys()
    
    uvicorn.run(
        planning_agent.to_a2a(),
        host="0.0.0.0",
        port=8005,
        reload=False,
        log_level="info"
    )
