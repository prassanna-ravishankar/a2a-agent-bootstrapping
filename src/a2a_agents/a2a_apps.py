"""A2A applications using Pydantic AI's built-in to_a2a() method."""

from .code_agent import code_agent
from .data_transformation_agent import data_transformation_agent
from .planning_agent import planning_agent
from .research_agent import research_agent

# Convert each agent to A2A-compliant ASGI applications
research_a2a_app = research_agent.to_a2a()
code_a2a_app = code_agent.to_a2a() 
data_a2a_app = data_transformation_agent.to_a2a()
planning_a2a_app = planning_agent.to_a2a()

# Export all A2A apps
__all__ = [
    "research_a2a_app",
    "code_a2a_app",
    "data_a2a_app", 
    "planning_a2a_app",
]
