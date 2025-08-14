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
from .code_agent import process_code_request, code_agent
from .data_transformation_agent import transform_data, data_transformation_agent
from .planning_agent import create_plan, planning_agent
from .research_agent import research_query, research_agent

# A2A applications
from .a2a_apps import (
    research_a2a_app,
    code_a2a_app,
    data_a2a_app,
    planning_a2a_app,
)

__version__ = "0.1.0"

# Agent information
AGENTS = {
    "research": {
        "name": "Research Agent",
        "emoji": "🕵️‍♂️",
        "description": "Answers complex queries by searching the web and synthesizing information",
        "a2a_app": research_a2a_app,
        "agent": research_agent,
        "function": research_query,
    },
    "code": {
        "name": "Code Agent", 
        "emoji": "💻",
        "description": "Generates new code or reviews code from GitHub repositories",
        "a2a_app": code_a2a_app,
        "agent": code_agent,
        "function": process_code_request,
    },
    "data": {
        "name": "Data Transformation Agent",
        "emoji": "🔄",
        "description": "Cleans and structures raw, messy data into specified formats",
        "a2a_app": data_a2a_app,
        "agent": data_transformation_agent,
        "function": transform_data,
    },
    "planning": {
        "name": "Logic and Planning Agent",
        "emoji": "🧠", 
        "description": "Breaks down high-level goals into logical, sequential plans",
        "a2a_app": planning_a2a_app,
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
    # A2A Applications
    "research_a2a_app", "code_a2a_app", "data_a2a_app", "planning_a2a_app",
]
