"""Comprehensive tests for A2A Agent Bootstrapping."""

import pytest
from fastapi.testclient import TestClient

from a2a_agents import AGENTS
from a2a_agents.models import (
    CodeGenerationRequest,
    DataTransformationRequest,
    PlanningRequest,
    ResearchQuery,
    TargetFormat,
    TaskType,
)
from modal_app import fastapi_app


@pytest.fixture
def client():
    """Test client for the FastAPI application."""
    return TestClient(fastapi_app)


class TestApplicationEndpoints:
    """Test main application endpoints."""

    def test_root_endpoint(self, client):
        """Test the root endpoint returns HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "A2A Agent Bootstrapping" in response.text

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "A2A Agent Bootstrapping"
        assert len(data["agents"]) == 4

    def test_agents_endpoint(self, client):
        """Test the agents listing endpoint."""
        response = client.get("/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["total_agents"] == 4
        assert len(data["agents"]) == 4


class TestResearchAgent:
    """Test Research Agent functionality."""

    def test_research_health_check(self, client):
        """Test research agent health check."""
        response = client.get("/research/health")
        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == "Research Agent 🕵️‍♂️"
        assert data["status"] == "healthy"

    def test_research_info_endpoint(self, client):
        """Test research agent info endpoint."""
        response = client.get("/research/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Research Agent"
        assert data["emoji"] == "🕵️‍♂️"
        assert "input_format" in data
        assert "output_format" in data

    def test_research_query_model(self):
        """Test research query model validation."""
        query = ResearchQuery(query="What is quantum computing?")
        assert query.query == "What is quantum computing?"

    @pytest.mark.asyncio
    async def test_research_query_function(self):
        """Test research query function basic structure."""
        from a2a_agents.research_agent import research_query
        
        query = ResearchQuery(query="Python programming")
        # Note: This would require API keys in a real test environment
        # For now, we just test the function exists and can be imported
        assert callable(research_query)


class TestCodeAgent:
    """Test Code Agent functionality."""

    def test_code_health_check(self, client):
        """Test code agent health check."""
        response = client.get("/code/health")
        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == "Code Agent 💻"
        assert data["status"] == "healthy"

    def test_code_info_endpoint(self, client):
        """Test code agent info endpoint."""
        response = client.get("/code/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Code Agent"
        assert data["emoji"] == "💻"
        assert "tasks" in data
        assert "generate" in data["tasks"]
        assert "review" in data["tasks"]

    def test_code_generation_model(self):
        """Test code generation model validation."""
        request = CodeGenerationRequest(
            task=TaskType.GENERATE,
            code_description="Create a function to calculate factorial"
        )
        assert request.task == TaskType.GENERATE
        assert "factorial" in request.code_description

    @pytest.mark.asyncio
    async def test_code_agent_function(self):
        """Test code agent function basic structure."""
        from a2a_agents.code_agent import process_code_request
        
        # Test that the function exists and can be imported
        assert callable(process_code_request)


class TestDataTransformationAgent:
    """Test Data Transformation Agent functionality."""

    def test_data_health_check(self, client):
        """Test data transformation agent health check."""
        response = client.get("/data/health")
        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == "Data Transformation Agent 🔄"
        assert data["status"] == "healthy"

    def test_data_info_endpoint(self, client):
        """Test data transformation agent info endpoint."""
        response = client.get("/data/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Data Transformation Agent"
        assert data["emoji"] == "🔄"
        assert "supported_input_formats" in data
        assert "supported_output_formats" in data

    def test_data_formats_endpoint(self, client):
        """Test data formats endpoint."""
        response = client.get("/data/formats")
        assert response.status_code == 200
        data = response.json()
        assert "supported_formats" in data
        assert "json" in data["supported_formats"]
        assert "csv" in data["supported_formats"]

    def test_data_transformation_model(self):
        """Test data transformation model validation."""
        request = DataTransformationRequest(
            data="name,age\nJohn,25\nJane,30",
            target_format=TargetFormat.JSON
        )
        assert request.target_format == TargetFormat.JSON
        assert "name,age" in request.data

    @pytest.mark.asyncio
    async def test_data_transformation_function(self):
        """Test data transformation function basic structure."""
        from a2a_agents.data_transformation_agent import transform_data
        
        # Test that the function exists and can be imported
        assert callable(transform_data)

    def test_target_format_enum(self):
        """Test TargetFormat enum values."""
        assert TargetFormat.JSON.value == "json"
        assert TargetFormat.CSV.value == "csv"
        assert TargetFormat.XML.value == "xml"
        assert TargetFormat.YAML.value == "yaml"
        assert TargetFormat.MARKDOWN.value == "markdown"
        assert TargetFormat.HTML.value == "html"


class TestPlanningAgent:
    """Test Logic and Planning Agent functionality."""

    def test_planning_health_check(self, client):
        """Test planning agent health check."""
        response = client.get("/planning/health")
        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == "Logic and Planning Agent 🧠"
        assert data["status"] == "healthy"

    def test_planning_info_endpoint(self, client):
        """Test planning agent info endpoint."""
        response = client.get("/planning/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Logic and Planning Agent"
        assert data["emoji"] == "🧠"
        assert "planning_approach" in data
        assert "step_characteristics" in data

    def test_planning_model(self):
        """Test planning model validation."""
        request = PlanningRequest(goal="Launch a mobile app")
        assert request.goal == "Launch a mobile app"

    @pytest.mark.asyncio
    async def test_planning_function(self):
        """Test planning function basic structure."""
        from a2a_agents.planning_agent import create_plan
        
        # Test that the function exists and can be imported
        assert callable(create_plan)

    def test_goal_complexity_analyzer(self):
        """Test goal complexity analysis utility."""
        from a2a_agents.planning_agent import analyze_goal_complexity
        
        simple_goal = "Write a blog post"
        complex_goal = "Develop a comprehensive enterprise software solution with microservices architecture"
        
        simple_analysis = analyze_goal_complexity(simple_goal)
        complex_analysis = analyze_goal_complexity(complex_goal)
        
        assert "Simple" in simple_analysis or "Moderate" in simple_analysis
        assert "Complex" in complex_analysis


class TestAgentRegistry:
    """Test the agent registry and metadata."""

    def test_agents_registry(self):
        """Test the AGENTS registry structure."""
        assert len(AGENTS) == 4
        assert "research" in AGENTS
        assert "code" in AGENTS
        assert "data" in AGENTS
        assert "planning" in AGENTS

    def test_agent_metadata_structure(self):
        """Test each agent has required metadata."""
        for agent_key, agent_info in AGENTS.items():
            assert "name" in agent_info
            assert "emoji" in agent_info
            assert "description" in agent_info
            assert "router" in agent_info
            assert "agent" in agent_info
            assert "function" in agent_info
            
            # Check that router and function are callable/valid
            assert hasattr(agent_info["router"], "prefix")  # FastAPI router
            assert callable(agent_info["function"])


class TestModels:
    """Test Pydantic models validation and structure."""

    def test_task_type_enum(self):
        """Test TaskType enum values."""
        assert TaskType.GENERATE.value == "generate"
        assert TaskType.REVIEW.value == "review"

    def test_model_imports(self):
        """Test that all models can be imported from the package."""
        from a2a_agents import (
            CodeAgentRequest,
            DataTransformationRequest, 
            PlanningRequest,
            ResearchQuery,
        )
        
        # Test basic instantiation
        research = ResearchQuery(query="test")
        assert research.query == "test"
        
        planning = PlanningRequest(goal="test goal")
        assert planning.goal == "test goal"


# Integration tests would require actual API keys and external services
# These are placeholder tests that verify the structure and basic functionality
@pytest.mark.integration
class TestIntegration:
    """Integration tests requiring external services (marked for optional running)."""

    @pytest.mark.skipif(
        True, reason="Requires API keys and external services - run manually with proper setup"
    )
    def test_full_research_pipeline(self, client):
        """Test full research pipeline (requires DuckDuckGo access)."""
        response = client.post(
            "/research/query",
            json={"query": "What is Python?"}
        )
        # This would work with proper API setup
        # assert response.status_code == 200

    @pytest.mark.skipif(
        True, reason="Requires Gemini API key - run manually with proper setup"
    )
    def test_full_planning_pipeline(self, client):
        """Test full planning pipeline (requires Gemini API)."""
        response = client.post(
            "/planning/plan",
            json={"goal": "Learn Python programming"}
        )
        # This would work with proper API setup
        # assert response.status_code == 200
