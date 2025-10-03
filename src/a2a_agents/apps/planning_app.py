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
def planning_agent_app():
    """Deploy Planning Agent - Pydantic AI handles everything!"""
    from ..agents.planning import planning_agent
    from ..config import config
    from starlette.responses import RedirectResponse
    from starlette.routing import Route

    config.setup_api_keys()

    # Get the base A2A app with custom title middleware
    from starlette.middleware import Middleware
    from .middleware import CustomTitleMiddleware

    # Get the dynamic Modal URL for this deployment
    agent_url = planning_agent_app.get_web_url()

    a2a_app = planning_agent.to_a2a(
        name="Planning Agent",
        url=agent_url,
        description="An AI agent specialized in project planning, task management, strategic planning, and workflow optimization",
        middleware=[Middleware(CustomTitleMiddleware, agent_name="Planning Agent")]
    )

    # Add root redirect to /docs
    async def redirect_to_docs(request):
        return RedirectResponse(url="/docs")

    a2a_app.routes.insert(0, Route("/", redirect_to_docs))

    return a2a_app

if __name__ == "__main__":
    import uvicorn
    from a2a_agents.agents.planning import planning_agent
    from a2a_agents.config import config
    from starlette.responses import RedirectResponse
    from starlette.routing import Route

    print("🧠 Starting Planning Agent locally on port 8005...")
    config.setup_api_keys()

    # Get the A2A app with custom title middleware
    from starlette.middleware import Middleware
    from a2a_agents.apps.middleware import CustomTitleMiddleware

    a2a_app = planning_agent.to_a2a(
        name="Planning Agent",
        url="http://localhost:8005",
        middleware=[Middleware(CustomTitleMiddleware, agent_name="Planning Agent")]
    )

    async def redirect_to_docs(request):
        return RedirectResponse(url="/docs")

    a2a_app.routes.insert(0, Route("/", redirect_to_docs))

    uvicorn.run(
        a2a_app,
        host="0.0.0.0",
        port=8005,
        reload=False,
        log_level="info"
    )
