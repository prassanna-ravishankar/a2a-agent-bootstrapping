# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an A2A (Agent-to-Agent) protocol implementation showcasing four specialized AI agents built with pydantic-ai. The agents communicate via the native A2A protocol and are deployed as a single FastAPI service on Modal.com.

## Architecture

The project implements four distinct agents, each with specific capabilities:
- **Research Agent**: Web search and information synthesis using DuckDuckGo
- **Code Agent**: Code generation and GitHub repository analysis using GitPython
- **Data Transformation Agent**: Data cleaning and format conversion (JSON/CSV/XML/YAML)
- **Planning Agent**: Strategic planning and goal decomposition

All agents are exposed via Pydantic AI's native `agent.to_a2a()` method for protocol compliance. The agents are mounted as ASGI sub-applications on a FastAPI server at `/research`, `/code`, `/data`, and `/planning` endpoints.

## Key Development Commands

```bash
# Run application locally
task run
# or directly
# Run individual agents (using module mode):
python -m a2a_agents.apps.research_app  # Port 8002
python -m a2a_agents.apps.code_app      # Port 8003
python -m a2a_agents.apps.data_app      # Port 8004
python -m a2a_agents.apps.planning_app  # Port 8005

# Run tests
task tests
# or with coverage
task coverage

# Code quality
task lint      # Fix linting issues with ruff
task format    # Format code with ruff
task type      # Type checking with ty

# Deploy to Modal.com (using module mode)
# Deploy individual agents:
modal deploy -m a2a_agents.apps.research_app
modal deploy -m a2a_agents.apps.code_app
modal deploy -m a2a_agents.apps.data_app
modal deploy -m a2a_agents.apps.planning_app
```

## Testing

Run specific test files:
```bash
pytest tests/test_a2a_agents.py -v
```

## Environment Setup

Required environment variable:
- `GEMINI_API_KEY`: Google AI Studio API key for Gemini model access

For Modal deployment, ensure the secret is configured:
```bash
modal secret create gemini-api-key GEMINI_API_KEY=your_key_here
```

## Code Organization

- `src/a2a_agents/`: Main package directory
  - `models.py`: Pydantic models for agent inputs/outputs
  - `config.py`: Configuration and API key setup
  - `agents/`: Core agent implementations
    - `research.py`, `code.py`, `data_transformation.py`, `planning.py`
  - `apps/`: Modal deployment applications
    - `research_app.py`, `code_app.py`, `data_app.py`, `planning_app.py`
  - `__init__.py`: Package exports and agent registry (AGENTS dict)

## Important Implementation Details

1. **A2A Protocol**: All agents use pydantic-ai's `to_a2a()` method for native protocol compliance
2. **Optimized Images**: Only the code agent includes git (for GitHub repository analysis), other agents use minimal images
3. **Error Handling**: Each agent has built-in error handling returning structured error responses
4. **Model Configuration**: Uses Gemini free tier (`gemini-2.0-flash-exp`) as the LLM backend
5. **CORS**: Enabled for all origins to support cross-domain A2A communication