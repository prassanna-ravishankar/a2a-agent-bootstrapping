"""
Simple Data Transformation Agent using Pydantic AI's built-in A2A support.
"""

import os
import modal
from dotenv import load_dotenv

load_dotenv()

app = modal.App("data-agent")

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
def data_agent_app():
    """Deploy Data Agent - Pydantic AI handles everything!"""
    from ..agents.data_transformation import data_transformation_agent
    from ..config import config
    
    config.setup_api_keys()
    return data_transformation_agent.to_a2a()

if __name__ == "__main__":
    import uvicorn
    from a2a_agents.agents.data_transformation import data_transformation_agent
    from a2a_agents.config import config
    
    print("🔄 Starting Data Agent locally on port 8004...")
    config.setup_api_keys()
    
    uvicorn.run(
        data_transformation_agent.to_a2a(),
        host="0.0.0.0",
        port=8004,
        reload=False,
        log_level="info"
    )
