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
    .pip_install_from_pyproject("pyproject.toml")
)

@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    timeout=30,  # Reduced from 60s to 30s to save costs
    max_containers=2,  # Limit concurrent containers to keep costs low
    scaledown_window=60,  # Scale down faster when idle (1 minute)
)
@modal.asgi_app()
def data_agent_app():
    """Deploy Data Agent - Pydantic AI handles everything!"""
    from ..agents.data_transformation import data_transformation_agent
    from ..config import config
    
    config.setup_api_keys()
    return data_transformation_agent.to_a2a(
        description="An AI agent specialized in data analysis, processing, visualization, and insights generation from various data sources"
    )

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
