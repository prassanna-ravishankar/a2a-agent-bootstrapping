# 🤖 A2A Agent Bootstrapping

> Bootstrap the `a2aregistry.org` with four specialized, highly capable, and application-agnostic agents using the A2A protocol.

A foundational showcase for building scalable and modular multi-agent systems featuring four distinct AI agents, each specialized in their domain with clear separation of concerns.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-red.svg)
![Modal](https://img.shields.io/badge/deployment-modal.com-purple.svg)

## 🎯 Project Overview

This project implements **four specialized AI agents** that demonstrate the power and flexibility of the A2A (Agent-to-Agent) protocol:

### 🕵️‍♂️ Research Agent
**Purpose**: Web search and information synthesis  
**Input**: Query string  
**Output**: Synthesized summary + source URLs  
**Capabilities**: DuckDuckGo search, multi-source analysis, fact synthesis

### 💻 Code Agent  
**Purpose**: Code generation and GitHub repository analysis  
**Input**: Task type + description OR GitHub URL  
**Output**: Generated code OR review summary with issues  
**Capabilities**: Natural language → code, repository analysis, issue detection

### 🔄 Data Transformation Agent
**Purpose**: Clean and structure messy data  
**Input**: Raw data + target format  
**Output**: Transformed structured data  
**Capabilities**: Multi-format parsing (JSON, CSV, XML, YAML), data cleaning, format conversion

### 🧠 Logic and Planning Agent
**Purpose**: Strategic planning and goal decomposition  
**Input**: High-level goal  
**Output**: Sequential actionable steps  
**Capabilities**: Goal analysis, task breakdown, dependency planning, strategic thinking

## 🛠️ Technology Stack

- **Agent Framework**: [pydantic-ai](https://github.com/pydantic/pydantic-ai) for A2A communication and agent logic
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) for creating the web service
- **Deployment**: [Modal.com](https://modal.com/) for serverless deployment
- **LLM**: Google Gemini (free tier) as the core reasoning engine
- **External Tools**: 
  - [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) for web research
  - [GitPython](https://gitpython.readthedocs.io/) for GitHub repository interactions
  - [HTTPX](https://www.python-httpx.org/) for async HTTP requests
  - [PyYAML](https://pyyaml.org/) for data transformation

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) for package management
- A [Google AI Studio API key](https://aistudio.google.com/) for Gemini access

### Local Development Setup

1. **Clone and navigate to the repository**
   ```bash
   git clone https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping.git
   cd a2a-agent-bootstrapping
   ```

2. **Create and activate virtual environment**
   ```bash
   uv venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux  
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   ```

5. **Run the application locally**
   ```bash
   # Run from the project root
   python -m a2a_agents.modal_app
   ```

6. **Open your browser**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### Deploy to Modal.com

1. **Install Modal CLI**
   ```bash
   pip install modal
   ```

2. **Authenticate with Modal**
   ```bash
   modal token new
   ```

3. **Set up secrets (CRITICAL for security)**
   ```bash
   # Create Modal secret for Gemini API key
   modal secret create gemini-api-key GEMINI_API_KEY=your_actual_gemini_key_here
   
   # Verify the secret was created
   modal secret list
   ```

4. **Deploy the application**
   ```bash
   # Deploy using module mode
   modal deploy -m a2a_agents.modal_app
   ```

## 📡 A2A Protocol Usage

All agents are exposed via **Pydantic AI's native A2A protocol**, providing standardized agent-to-agent communication:

### Research Agent
```bash
curl -X POST "http://localhost:8000/research/" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest developments in quantum computing?"}'
```

### Code Agent
```bash
curl -X POST "http://localhost:8000/code/" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "generate",
    "code_description": "Create a Python function to calculate Fibonacci numbers efficiently"
  }'
```

### Data Transformation Agent
```bash
curl -X POST "http://localhost:8000/data/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "name,age,city\nJohn,25,New York\nJane,30,Boston",
    "target_format": "json"
  }'
```

### Planning Agent
```bash
curl -X POST "http://localhost:8000/planning/" \
  -H "Content-Type: application/json" \
  -d '{"goal": "Launch a mobile app for task management"}'
```

> **Note**: All endpoints follow the A2A protocol specification, enabling seamless agent-to-agent communication across different systems.

## 🏗️ Project Architecture

```
a2a-agent-bootstrapping/
├── src/
│   └── a2a_agents/
│       ├── __init__.py       # Package exports and agent registry
│       ├── modal_app.py      # Main FastAPI application + Modal deployment
│       ├── models.py         # Pydantic models for A2A communication
│       ├── a2a_apps.py      # A2A applications using agent.to_a2a()
│       ├── research_agent.py # Research Agent core logic
│       ├── code_agent.py     # Code Agent core logic  
│       ├── data_transformation_agent.py # Data Agent core logic
│       └── planning_agent.py # Planning Agent core logic
├── tests/                    # Comprehensive test suite
├── pyproject.toml           # Project configuration and dependencies
└── README.md               # This file
```

### Design Principles

1. **Pure A2A Protocol Implementation**: All agents are exposed via Pydantic AI's native `agent.to_a2a()` method for true protocol compliance.

2. **Modular Agent Design**: Each agent is self-contained with its own logic and A2A application, making the system highly maintainable and extensible.

3. **Single Unified Deployment**: All agents are deployed together as one FastAPI service for efficient resource sharing and simplified CI/CD.

4. **Protocol-First Approach**: Built specifically for agent-to-agent communication, not human-facing APIs.

5. **Modal.com Integration**: Secure secrets management and serverless deployment for production readiness.

## 🧪 Development Commands

We use [taskipy](https://github.com/taskipy/taskipy) for common development tasks:

```bash
# Run the application locally
task run

# Run all tests
task tests

# Run tests with coverage report
task coverage

# Type checking
task type

# Code linting
task lint

# Code formatting  
task format
```

### Testing

The project includes comprehensive tests covering:

- **Unit Tests**: Individual agent functions and models
- **A2A Protocol Tests**: Native Pydantic AI agent functionality
- **Structure Tests**: Agent registry, model validation, and package organization
- **Application Tests**: Main FastAPI application and core endpoints

Run tests with:
```bash
pytest
# or
task tests

# With coverage
pytest --cov=src/a2a_agents --cov-report=html
# or  
task coverage
```

## 🌟 Key Features

### ✅ A2A Protocol Compliant
- Native Pydantic AI `agent.to_a2a()` implementation
- Standardized agent-to-agent communication
- Interoperable with other A2A systems
- Protocol-first design approach

### ✅ Production Ready
- Comprehensive error handling and validation
- Modal secrets for secure API key management
- Structured logging and monitoring ready
- Comprehensive test coverage

### ✅ Scalable Architecture  
- Modular agent design for easy extension
- Single deployment model for efficiency
- Clean separation of concerns
- Serverless scaling with Modal.com

### ✅ Developer Experience
- Type hints throughout the codebase
- Comprehensive test suite covering A2A functionality
- Easy local development setup
- Clear project structure and documentation

## 📊 Agent Capabilities Matrix

| Agent | Web Search | Code Gen | Code Review | Data Parsing | Planning | GitHub Integration |
|-------|------------|----------|-------------|--------------|----------|-------------------|
| Research 🕵️‍♂️ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Code 💻 | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Data 🔄 | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Planning 🧠 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Contact & Support

- **Author**: [Prass, The Nomadic Coder](https://github.com/prassanna-ravishankar)
- **Email**: contact@a2aregistry.org
- **Issues**: [GitHub Issues](https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping/issues)
- **Documentation**: [GitHub Pages](https://github.com/prassanna-ravishankar/a2a-agent-bootstrapping)

## 🌟 Acknowledgments

- Built with [pydantic-ai](https://github.com/pydantic/pydantic-ai) for A2A protocol support
- Powered by [Google Gemini](https://ai.google.dev/) for intelligent reasoning
- Deployed on [Modal.com](https://modal.com/) for serverless excellence
- UI inspiration from modern web design practices

---

**Ready to bootstrap your multi-agent system?** 🚀  
Start exploring the agents at [localhost:8000](http://localhost:8000) after setup!
