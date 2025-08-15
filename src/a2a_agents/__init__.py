"""A2A Agent Bootstrapping - Four specialized agents for the A2A protocol."""

# Models for A2A communication
from .models import (
    CodeAgentRequest,
    CodeAgentResult,
    CodeGenerationRequest,
    CodeGenerationResult,
    CodeIssue,
    CodeReviewRequest,
    CodeReviewResult,
    DataTransformationRequest,
    DataTransformationResult,
    PlanningRequest,
    PlanningResult,
    ResearchQuery,
    ResearchResult,
    TargetFormat,
    TaskType,
)

# Agent core logic functions
from .agents.code import process_code_request, code_agent
from .agents.data_transformation import transform_data, data_transformation_agent
from .agents.planning import create_plan, planning_agent
from .agents.research import research_query, research_agent

# Configuration
from .config import config

__version__ = "0.1.0"

# Agent information
AGENTS = {
    "research": {
        "name": "Research Agent",
        "emoji": "🕵️‍♂️",
        "description": "Answers complex queries by searching the web and synthesizing information",
        "modal_app": "apps/research_app.py",
        "agent": research_agent,
        "function": research_query,
    },
    "code": {
        "name": "Code Agent", 
        "emoji": "💻",
        "description": "Generates new code or reviews code from GitHub repositories",
        "modal_app": "apps/code_app.py",
        "agent": code_agent,
        "function": process_code_request,
    },
    "data": {
        "name": "Data Transformation Agent",
        "emoji": "🔄",
        "description": "Cleans and structures raw, messy data into specified formats",
        "modal_app": "apps/data_app.py",
        "agent": data_transformation_agent,
        "function": transform_data,
    },
    "planning": {
        "name": "Logic and Planning Agent",
        "emoji": "🧠", 
        "description": "Breaks down high-level goals into logical, sequential plans",
        "modal_app": "apps/planning_app.py",
        "agent": planning_agent,
        "function": create_plan,
    }
}

__all__ = [
    # Version
    "__version__",
    # Agent registry
    "AGENTS",
    # Models
    "ResearchQuery", "ResearchResult",
    "CodeGenerationRequest", "CodeReviewRequest", "CodeAgentRequest", 
    "CodeGenerationResult", "CodeReviewResult", "CodeAgentResult", "CodeIssue",
    "DataTransformationRequest", "DataTransformationResult", "TargetFormat",
    "PlanningRequest", "PlanningResult", 
    "TaskType",
    # Agent functions
    "research_query", "research_agent",
    "process_code_request", "code_agent", 
    "transform_data", "data_transformation_agent",
    "create_plan", "planning_agent",
    # Configuration
    "config",
]
