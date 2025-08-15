"""
Simple Code Agent using Pydantic AI's built-in A2A support.
"""

import os
import modal
from dotenv import load_dotenv

load_dotenv()

app = modal.App("simple-code-agent")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Required for GitPython
    .pip_install_from_pyproject("pyproject.toml")
)

@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    container_idle_timeout=300,
    timeout=60,
)
@modal.asgi_app()
def simple_code_agent():
    """Deploy Code Agent - Pydantic AI handles everything!"""
    from .code_agent import code_agent
    from .config import config
    
    config.setup_api_keys()
    return code_agent.to_a2a()

if __name__ == "__main__":
    import uvicorn
    from src.a2a_agents.code_agent import code_agent
    from src.a2a_agents.config import config
    
    print("💻 Starting Code Agent locally on port 8003...")
    config.setup_api_keys()
    
    uvicorn.run(
        code_agent.to_a2a(),
        host="0.0.0.0",
        port=8003,
        reload=False,
        log_level="info"
    )
