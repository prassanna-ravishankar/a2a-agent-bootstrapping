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
    timeout=30,  # Reduced from 60s to 30s to save costs
    max_containers=2,  # Limit concurrent containers to keep costs low
    scaledown_window=60,  # Scale down faster when idle (1 minute)
)
@modal.asgi_app()
def code_agent_app():
    """Deploy Code Agent - Pydantic AI handles everything!"""
    from ..agents.code import code_agent
    from ..config import config
    from starlette.responses import RedirectResponse
    from starlette.routing import Route

    config.setup_api_keys()

    # Get the base A2A app
    a2a_app = code_agent.to_a2a(
        name="Code Agent",
        description="An AI agent specialized in code generation, review, debugging, and software development assistance"
    )

    # Add root redirect to /docs
    async def redirect_to_docs(request):
        return RedirectResponse(url="/docs")

    a2a_app.routes.insert(0, Route("/", redirect_to_docs))

    return a2a_app

if __name__ == "__main__":
    import uvicorn
    from a2a_agents.agents.code import code_agent
    from a2a_agents.config import config
    from starlette.responses import RedirectResponse
    from starlette.routing import Route

    print("💻 Starting Code Agent locally on port 8003...")
    config.setup_api_keys()

    # Get the A2A app and add root redirect
    a2a_app = code_agent.to_a2a(name="Code Agent")

    async def redirect_to_docs(request):
        return RedirectResponse(url="/docs")

    a2a_app.routes.insert(0, Route("/", redirect_to_docs))

    uvicorn.run(
        a2a_app,
        host="0.0.0.0",
        port=8003,
        reload=False,
        log_level="info"
    )
