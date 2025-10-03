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
    .pip_install_from_pyproject("pyproject.toml")  # Use root dependencies
)


@app.function(
    image=image,
    secrets=[modal.Secret.from_dict({"GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "")})],
    timeout=30,  # Reduced from 60s to 30s to save costs
    max_containers=2,  # Limit concurrent containers to keep costs low
    scaledown_window=60,  # Scale down faster when idle (1 minute)
)
@modal.asgi_app()
def research_agent_app():
    """Deploy Research Agent with custom A2A metadata!"""
    from ..agents.research import research_agent
    from ..config import config
    from starlette.responses import RedirectResponse
    from starlette.routing import Route

    config.setup_api_keys()

    # Get the base A2A app with custom title middleware
    from starlette.middleware import Middleware
    from .middleware import CustomTitleMiddleware

    # Get the dynamic Modal URL for this deployment
    agent_url = research_agent_app.get_web_url()

    a2a_app = research_agent.to_a2a(
        name="Research Agent",
        url=agent_url,
        description="An AI agent specialized in research tasks, information gathering, and analysis using advanced search and synthesis capabilities",
        middleware=[Middleware(CustomTitleMiddleware, agent_name="Research Agent")]
    )

    # Add root redirect to /docs
    async def redirect_to_docs(request):
        return RedirectResponse(url="/docs")

    a2a_app.routes.insert(0, Route("/", redirect_to_docs))

    return a2a_app


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    from a2a_agents.agents.research import research_agent
    from a2a_agents.config import config
    from starlette.responses import RedirectResponse
    from starlette.routing import Route

    print("🕵️‍♂️ Starting Research Agent locally on port 8002...")
    config.setup_api_keys()

    # Get the A2A app with custom title middleware
    from starlette.middleware import Middleware
    from a2a_agents.apps.middleware import CustomTitleMiddleware

    a2a_app = research_agent.to_a2a(
        name="Research Agent",
        url="http://localhost:8002",
        middleware=[Middleware(CustomTitleMiddleware, agent_name="Research Agent")]
    )

    async def redirect_to_docs(request):
        return RedirectResponse(url="/docs")

    a2a_app.routes.insert(0, Route("/", redirect_to_docs))

    uvicorn.run(
        a2a_app,
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )
