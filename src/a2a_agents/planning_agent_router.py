"""FastAPI router for the Logic and Planning Agent."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .models import PlanningRequest, PlanningResult
from .planning_agent import create_plan


# Create the router for the Planning Agent
planning_router = APIRouter(
    prefix="/planning",
    tags=["planning"],
    responses={404: {"description": "Not found"}},
)


@planning_router.post("/plan", response_model=PlanningResult)
async def planning_endpoint(request: PlanningRequest) -> PlanningResult:
    """Logic and Planning Agent endpoint for goal breakdown.
    
    Args:
        request: Planning request with goal
        
    Returns:
        Planning result with sequential actionable steps
    """
    try:
        result = await create_plan(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning failed: {str(e)}")


@planning_router.post("/analyze")
async def analyze_goal_endpoint(request: PlanningRequest):
    """Analyze a goal without creating a full plan.
    
    Args:
        request: Planning request with goal to analyze
        
    Returns:
        Goal analysis results
    """
    try:
        from .planning_agent import analyze_goal_complexity
        
        analysis = analyze_goal_complexity(request.goal)
        
        return JSONResponse(
            content={
                "goal": request.goal,
                "analysis": analysis,
                "recommendations": [
                    "Consider breaking down complex goals into smaller milestones",
                    "Identify key dependencies and prerequisites",
                    "Plan for validation and review phases",
                    "Account for potential risks and contingencies"
                ]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Goal analysis failed: {str(e)}")


@planning_router.get("/health")
async def planning_health_check():
    """Health check endpoint for the Planning Agent."""
    return JSONResponse(
        status_code=200,
        content={
            "agent": "Logic and Planning Agent 🧠",
            "status": "healthy",
            "capabilities": [
                "Goal analysis and complexity assessment",
                "Strategic planning and decomposition",
                "Step sequencing with dependencies",
                "Risk and contingency planning"
            ]
        }
    )


@planning_router.get("/info")
async def planning_info():
    """Information endpoint for the Planning Agent."""
    return JSONResponse(
        content={
            "name": "Logic and Planning Agent",
            "emoji": "🧠",
            "description": "Breaks down high-level goals into logical, sequential plans of actionable steps",
            "input_format": {
                "goal": "string - High-level goal to break down into steps"
            },
            "output_format": {
                "steps": "array - Sequential list of actionable steps"
            },
            "planning_approach": [
                "Goal Analysis - Understand scope and context",
                "Decomposition - Break into manageable components", 
                "Sequencing - Order tasks by dependencies",
                "Specificity - Make steps concrete and actionable",
                "Validation - Ensure comprehensive and realistic plan"
            ],
            "step_characteristics": [
                "Start with action verbs (Create, Develop, Test, etc.)",
                "Specific and measurable outcomes",
                "Consider dependencies and prerequisites",
                "Include validation and review phases",
                "Account for risks and contingencies"
            ],
            "example_input": {
                "goal": "Launch a mobile app for task management"
            },
            "example_output": {
                "steps": [
                    "Define app requirements and target audience",
                    "Create wireframes and UI/UX designs",
                    "Develop core functionality and features",
                    "Implement user authentication and data storage",
                    "Conduct thorough testing and bug fixes",
                    "Deploy to app stores and launch marketing campaign"
                ]
            }
        }
    )


# Export the router
__all__ = ['planning_router']
