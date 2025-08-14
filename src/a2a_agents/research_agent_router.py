"""FastAPI router for the Research Agent."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .models import ResearchQuery, ResearchResult
from .research_agent import research_query


# Create the router for the Research Agent
research_router = APIRouter(
    prefix="/research",
    tags=["research"],
    responses={404: {"description": "Not found"}},
)


@research_router.post("/query", response_model=ResearchResult)
async def research_endpoint(query: ResearchQuery) -> ResearchResult:
    """Research Agent endpoint for web search and information synthesis.
    
    Args:
        query: Research query input
        
    Returns:
        Research results with summary and source URLs
    """
    try:
        result = await research_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")


@research_router.get("/health")
async def research_health_check():
    """Health check endpoint for the Research Agent."""
    return JSONResponse(
        status_code=200,
        content={
            "agent": "Research Agent 🕵️‍♂️",
            "status": "healthy",
            "capabilities": [
                "Web search using DuckDuckGo",
                "Information synthesis",
                "Source citation"
            ]
        }
    )


@research_router.get("/info")
async def research_info():
    """Information endpoint for the Research Agent."""
    return JSONResponse(
        content={
            "name": "Research Agent",
            "emoji": "🕵️‍♂️",
            "description": "Answers complex queries by searching the web and synthesizing information",
            "input_format": {
                "query": "string - The research query to investigate"
            },
            "output_format": {
                "summary": "string - Synthesized summary of research findings",
                "source_urls": "array - List of source URLs used in research"
            },
            "example_input": {
                "query": "What are the latest developments in quantum computing?"
            }
        }
    )


# Export the router
__all__ = ['research_router']
