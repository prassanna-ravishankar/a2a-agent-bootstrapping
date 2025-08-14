"""FastAPI router for the Code Agent."""

from typing import Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .code_agent import process_code_request
from .models import (
    CodeAgentRequest,
    CodeAgentResult,
    CodeGenerationRequest,
    CodeReviewRequest,
)


# Create the router for the Code Agent
code_router = APIRouter(
    prefix="/code",
    tags=["code"],
    responses={404: {"description": "Not found"}},
)


@code_router.post("/process", response_model=CodeAgentResult)
async def code_endpoint(request: CodeAgentRequest) -> CodeAgentResult:
    """Code Agent endpoint for code generation and review.
    
    Args:
        request: Code agent request (generation or review)
        
    Returns:
        Code agent result (generated code or review summary)
    """
    try:
        result = await process_code_request(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code processing failed: {str(e)}")


@code_router.post("/generate")
async def code_generate_endpoint(request: CodeGenerationRequest):
    """Specific endpoint for code generation.
    
    Args:
        request: Code generation request
        
    Returns:
        Generated code result
    """
    try:
        result = await process_code_request(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")


@code_router.post("/review")
async def code_review_endpoint(request: CodeReviewRequest):
    """Specific endpoint for code review.
    
    Args:
        request: Code review request
        
    Returns:
        Code review result with issues
    """
    try:
        result = await process_code_request(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code review failed: {str(e)}")


@code_router.get("/health")
async def code_health_check():
    """Health check endpoint for the Code Agent."""
    return JSONResponse(
        status_code=200,
        content={
            "agent": "Code Agent 💻",
            "status": "healthy",
            "capabilities": [
                "Code generation from descriptions",
                "GitHub repository review",
                "Issue detection and analysis"
            ]
        }
    )


@code_router.get("/info")
async def code_info():
    """Information endpoint for the Code Agent."""
    return JSONResponse(
        content={
            "name": "Code Agent",
            "emoji": "💻",
            "description": "Generates new code or reviews code from GitHub repositories",
            "tasks": {
                "generate": {
                    "input_format": {
                        "task": "string - 'generate'",
                        "code_description": "string - Description of code to generate"
                    },
                    "output_format": {
                        "generated_code": "string - The generated code"
                    }
                },
                "review": {
                    "input_format": {
                        "task": "string - 'review'",
                        "github_url": "string - GitHub repository URL",
                        "branch": "string - Optional branch name"
                    },
                    "output_format": {
                        "review_summary": "string - Summary of the code review",
                        "issues": "array - List of issues found with severity levels"
                    }
                }
            },
            "example_inputs": {
                "generation": {
                    "task": "generate",
                    "code_description": "Create a Python function to calculate Fibonacci numbers"
                },
                "review": {
                    "task": "review",
                    "github_url": "https://github.com/user/repo",
                    "branch": "main"
                }
            }
        }
    )


# Export the router
__all__ = ['code_router']
