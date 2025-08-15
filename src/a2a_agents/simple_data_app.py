"""
Simple Data Transformation Agent using Pydantic AI's built-in A2A support.
"""

import os
import modal
from dotenv import load_dotenv

load_dotenv()

app = modal.App("simple-data-agent")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Required for potential git operations
    .pip_install_from_pyproject("pyproject.toml")
)

@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    container_idle_timeout=300,
    timeout=60,
)
@modal.asgi_app()
def simple_data_agent():
    """Deploy Data Agent using Pydantic AI's native A2A support."""
    from .data_transformation_agent import data_transformation_agent
    from .config import config
    
    config.setup_api_keys()
    print("🔄 Data Agent ready with native A2A protocol")
    return data_transformation_agent.to_a2a()

if __name__ == "__main__":
    import uvicorn
    from src.a2a_agents.data_transformation_agent import data_transformation_agent
    from src.a2a_agents.config import config
    
    print("🔄 Starting Simple Data Agent on port 8004...")
    config.setup_api_keys()
    
    uvicorn.run(
        data_transformation_agent.to_a2a(),
        host="0.0.0.0", 
        port=8004,
        reload=False,
        log_level="info"
    )
