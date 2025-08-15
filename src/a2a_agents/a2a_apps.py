"""A2A applications using FastA2A's built-in PydanticAI integration.

Note: FastA2A docs pages (e.g., /research/docs) are not fully compatible with 
multi-agent mounted systems. They may show "Failed to load agent information"
because they expect a single agent at the root domain. Use individual agent 
cards (/.well-known/agent.json) for proper A2A discovery instead.
"""

from .code_agent import code_agent
from .data_transformation_agent import data_transformation_agent
from .planning_agent import planning_agent
from .research_agent import research_agent

# Convert each PydanticAI agent to independent A2A-compliant FastA2A applications
# Each agent gets its own URL, name, and capabilities for independent discovery
research_a2a_app = research_agent.to_a2a(
    name="Research Agent",
    url="http://localhost:8000/research",
    version="1.0.0",
    description="Web search and information synthesis using DuckDuckGo API",
    provider={
        "name": "A2A Agent Bootstrapping",
        "url": "https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping",
    },
    skills=[
        {"name": "web_search", "description": "Search the web for information using DuckDuckGo"},
        {"name": "information_synthesis", "description": "Synthesize information from sources"},
        {"name": "source_citation", "description": "Provide citations for information sources"},
    ],
)

code_a2a_app = code_agent.to_a2a(
    name="Code Agent",
    url="http://localhost:8000/code",
    version="1.0.0", 
    description="Code generation and GitHub repository analysis using GitPython",
    provider={
        "name": "A2A Agent Bootstrapping",
        "url": "https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping"
    },
    skills=[
        {"name": "code_generation", "description": "Generate code from natural language descriptions"},
        {"name": "repository_analysis", "description": "Analyze GitHub repositories for structure and issues"},
        {"name": "code_review", "description": "Review code for potential improvements and issues"}
    ]
)

data_a2a_app = data_transformation_agent.to_a2a(
    name="Data Transformation Agent",
    url="http://localhost:8000/data",
    version="1.0.0",
    description="Data cleaning and format transformation (JSON/CSV/XML/YAML)",
    provider={
        "name": "A2A Agent Bootstrapping", 
        "url": "https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping"
    },
    skills=[
        {"name": "data_parsing", "description": "Parse and understand various data formats"},
        {"name": "format_conversion", "description": "Convert data between JSON, CSV, XML, YAML formats"},
        {"name": "data_cleaning", "description": "Clean and normalize messy or inconsistent data"}
    ]
)

planning_a2a_app = planning_agent.to_a2a(
    name="Logic and Planning Agent", 
    url="http://localhost:8000/planning",
    version="1.0.0",
    description="Strategic planning and goal decomposition into actionable steps",
    provider={
        "name": "A2A Agent Bootstrapping",
        "url": "https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping"
    },
    skills=[
        {"name": "goal_analysis", "description": "Analyze complex goals and objectives"},
        {"name": "task_decomposition", "description": "Break down goals into logical, sequential steps"},
        {"name": "strategic_planning", "description": "Create comprehensive plans with timelines and dependencies"}
    ]
)

# Export all A2A apps
__all__ = [
    "research_a2a_app",
    "code_a2a_app",
    "data_a2a_app", 
    "planning_a2a_app",
]
