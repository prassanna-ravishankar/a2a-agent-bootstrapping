"""
Simple Code Agent using Pydantic AI's built-in A2A support.
"""

import os
import modal
from dotenv import load_dotenv

load_dotenv()

app = modal.App("code-agent")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")  # Required for GitPython (GitHub repository analysis)
    .pip_install_from_pyproject("pyproject.toml")
)

@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    scaledown_window=300,
    timeout=60,
)
@modal.asgi_app()
def code_agent_app():
    """Deploy Code Agent - Pydantic AI handles everything!"""
    from ..agents.code import code_agent
    from ..config import config
    
    config.setup_api_keys()
    return code_agent.to_a2a(
        description="An AI agent specialized in code generation, review, debugging, and software development assistance"
    )

if __name__ == "__main__":
    import uvicorn
    from a2a_agents.agents.code import code_agent
    from a2a_agents.config import config
    
    print("💻 Starting Code Agent locally on port 8003...")
    config.setup_api_keys()
    
    uvicorn.run(
        code_agent.to_a2a(),
        host="0.0.0.0",
        port=8003,
        reload=False,
        log_level="info"
    )
