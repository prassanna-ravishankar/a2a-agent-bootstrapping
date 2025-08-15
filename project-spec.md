## 1\. Project Overview and Goal

**Project Name**: a2a-agent-bootstrapping

**Project Goal**: To bootstrap the `a2aregistry.org` with four specialized, highly capable, and application-agnostic agents. This project will serve as a foundational showcase for building scalable and modular multi-agent systems using the A2A protocol.

**Core Technologies**:

  * **Agent Framework**: `pydantic-ai` for A2A communication and agent logic.
  * **Web Framework**: `FastAPI` for creating the web service.
  * **Hosting**: `modal.com` for simplified, serverless deployment.
  * **LLM**: Gemini (free tier) as the core reasoning engine for all agents.
  * **External Tools**: DuckDuckGo API for web searches and `GitPython` for GitHub repository interactions.

-----

## 2\. Agent Roster and Responsibilities

This project will implement four distinct agents. Each is an expert in its domain, with a clear separation of concerns.

| Agent | Purpose | Key Inputs | Key Outputs |
| :--- | :--- | :--- | :--- |
| **Research Agent 🕵️‍♂️** | Answers a complex query by searching the web and synthesizing information. | A `query` string. | A `summary` string and a list of `source_urls`. |
| **Code Agent 💻** | Generates new code or reviews code from a GitHub repository. | A `task` (generate/review) and either a `code_description` or a `github_url` with an optional `branch`. | A `generated_code` string or a `review_summary` string with a list of `issues`. |
| **Data Transformation Agent 🔄** | Cleans and structures raw, messy data into a specified format. | Raw `data` (text or URL) and a `target_format` (e.g., "JSON"). | A string representing the `transformed_data`. |
| **Logic and Planning Agent 🧠** | Breaks down a high-level goal into a logical, sequential plan of actionable steps. | A `goal` string. | A list of `steps`, where each step is a string describing a task. |

-----

## 3\. Project Structure

The project will follow the `wyattferguson/pattern` cookiecutter, with an additional `a2a_agents` subpackage to organize the agent-specific code. This structure promotes modularity and makes the project easy to navigate.

```
/a2a-agent-bootstrapping
├── .env                  # For API keys and other secrets
├── pyproject.toml
├── requirements.txt
├── apps/                     # Modal deployment applications
│   ├── research_app.py       # Research Agent Modal deployment
│   ├── code_app.py           # Code Agent Modal deployment  
│   ├── data_app.py           # Data Agent Modal deployment
│   └── planning_app.py       # Planning Agent Modal deployment
├── agents/                   # Core agent implementations
│   ├── research.py           # Research Agent core logic
│   ├── code.py               # Code Agent core logic
│   ├── data_transformation.py# Data Agent core logic
│   └── planning.py           # Planning Agent core logic
└── src/
    └── a2a_agents/
        ├── __init__.py
        ├── models.py                   # Pydantic models for A2A communication
        ├── research_agent.py           # Research Agent core logic
        ├── code_agent.py               # Code Agent core logic
        ├── data_transformation_agent.py# Data Transformation Agent core logic
        ├── planning_agent.py           # Logic and Planning Agent core logic
        ├── agents/                     # Core agent implementations
        │   ├── research.py             # Research Agent core logic
        │   ├── code.py                 # Code Agent core logic
        │   ├── data_transformation.py  # Data Agent core logic
        │   └── planning.py             # Planning Agent core logic
        └── apps/                       # Modal deployment applications
            ├── research_app.py         # Research Agent Modal deployment
            ├── code_app.py             # Code Agent Modal deployment
            ├── data_app.py             # Data Agent Modal deployment
            └── planning_app.py         # Planning Agent Modal deployment
```

-----

## 4\. Communication and Deployment Strategy

The project is built on the principle of **individual modal applications per agent** for independent deployment and scaling.

### A. Individual Agent Applications

Each agent's core logic is a `pydantic_ai.Agent` instance. The `pydantic-ai` library's `to_a2a()` method is used to automatically generate a complete ASGI application for each agent. This application handles all the necessary A2A endpoints, including task submission and status checking. This approach allows each agent to be treated as a completely independent, self-contained service.

### B. Separate Modal Applications

Each agent has its own Modal application file (`*_app.py` in the `apps/` directory) that can be deployed independently. Each file defines its own `modal.App`, `modal.Image`, and deployment configuration. This allows for:
- Independent scaling per agent
- Separate deployment cycles
- Isolated resource management
- Individual monitoring and logging

### C. Modal.com Hosting

Each `*_app.py` file in the `apps/` directory serves as an independent deployment entry point. Each defines its own `modal.App` with appropriate dependencies and secrets. The agents are deployed using the `@modal.asgi_app()` decorator, which efficiently hosts each service on its own container.

This deployment model provides maximum flexibility because each agent can be scaled, updated, and managed independently, allowing for optimal resource utilization and deployment strategies per agent type.