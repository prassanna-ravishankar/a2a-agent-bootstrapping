"""Shared middleware for A2A agent applications."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class CustomTitleMiddleware(BaseHTTPMiddleware):
    """Middleware to customize the title and heading in the /docs page."""

    def __init__(self, app, agent_name: str):
        super().__init__(app)
        self.agent_name = agent_name

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path == "/docs" and response.status_code == 200:
            # Read and modify HTML content
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            content = body.decode('utf-8')

            # Replace title and heading with custom agent name
            modified_content = content.replace("<title>FastA2A Agent</title>", f"<title>{self.agent_name}</title>")
            modified_content = modified_content.replace("<h1>🤖 FastA2A Agent</h1>", f"<h1>🤖 {self.agent_name}</h1>")

            # Create new response with updated content-length
            headers = dict(response.headers)
            headers['content-length'] = str(len(modified_content.encode('utf-8')))

            return Response(
                content=modified_content,
                status_code=response.status_code,
                headers=headers,
                media_type="text/html"
            )
        return response
