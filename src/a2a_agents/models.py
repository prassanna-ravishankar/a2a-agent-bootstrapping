"""Pydantic models for A2A communication between agents."""

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class TaskType(str, Enum):
    """Task types for the Code Agent."""
    GENERATE = "generate"
    REVIEW = "review"


class TargetFormat(str, Enum):
    """Target formats for the Data Transformation Agent."""
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    YAML = "yaml"
    MARKDOWN = "markdown"
    HTML = "html"


# Research Agent Models
class ResearchQuery(BaseModel):
    """Input model for the Research Agent."""
    query: str = Field(..., description="The research query to investigate")


class ResearchResult(BaseModel):
    """Output model for the Research Agent."""
    summary: str = Field(..., description="Synthesized summary of research findings")
    source_urls: List[HttpUrl] = Field(..., description="List of source URLs used in research")


# Code Agent Models
class CodeGenerationRequest(BaseModel):
    """Input model for code generation task."""
    task: TaskType = Field(..., description="Type of task to perform")
    code_description: str = Field(..., description="Description of code to generate")


class CodeReviewRequest(BaseModel):
    """Input model for code review task."""
    task: TaskType = Field(..., description="Type of task to perform")
    github_url: HttpUrl = Field(..., description="GitHub repository URL to review")
    branch: Optional[str] = Field(None, description="Branch to review (defaults to main)")


class CodeIssue(BaseModel):
    """Model representing a code issue found during review."""
    severity: str = Field(..., description="Issue severity (low, medium, high, critical)")
    description: str = Field(..., description="Description of the issue")
    file_path: Optional[str] = Field(None, description="File path where issue was found")
    line_number: Optional[int] = Field(None, description="Line number where issue was found")


class CodeGenerationResult(BaseModel):
    """Output model for code generation."""
    generated_code: str = Field(..., description="The generated code")


class CodeReviewResult(BaseModel):
    """Output model for code review."""
    review_summary: str = Field(..., description="Summary of the code review")
    issues: List[CodeIssue] = Field(..., description="List of issues found")


# Data Transformation Agent Models
class DataTransformationRequest(BaseModel):
    """Input model for the Data Transformation Agent."""
    data: str = Field(..., description="Raw data to transform (text or URL)")
    target_format: TargetFormat = Field(..., description="Target format for transformation")


class DataTransformationResult(BaseModel):
    """Output model for the Data Transformation Agent."""
    transformed_data: str = Field(..., description="The transformed data in the requested format")


# Planning Agent Models
class PlanningRequest(BaseModel):
    """Input model for the Logic and Planning Agent."""
    goal: str = Field(..., description="High-level goal to break down into steps")


class PlanningResult(BaseModel):
    """Output model for the Logic and Planning Agent."""
    steps: List[str] = Field(..., description="Sequential list of actionable steps")


# Unified Code Agent Request Model
class CodeAgentRequest(BaseModel):
    """Unified input model for the Code Agent."""
    task: TaskType = Field(..., description="Type of task to perform")
    code_description: Optional[str] = Field(None, description="Description of code to generate (for GENERATE tasks)")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub repository URL to review (for REVIEW tasks)")
    branch: Optional[str] = Field(None, description="Branch to review (defaults to main)")
    
    def model_validate(cls, data):
        """Validate that required fields are present based on task type."""
        if isinstance(data, dict):
            task = data.get('task')
            if task == TaskType.GENERATE and not data.get('code_description'):
                raise ValueError("code_description is required for GENERATE tasks")
            elif task == TaskType.REVIEW and not data.get('github_url'):
                raise ValueError("github_url is required for REVIEW tasks")
        return super().model_validate(data)

# Unified Code Agent Result Model  
class CodeAgentResult(BaseModel):
    """Unified output model for the Code Agent."""
    task: TaskType = Field(..., description="Type of task that was performed")
    generated_code: Optional[str] = Field(None, description="The generated code (for GENERATE tasks)")
    review_summary: Optional[str] = Field(None, description="Summary of the code review (for REVIEW tasks)")
    issues: Optional[List[CodeIssue]] = Field(None, description="List of issues found (for REVIEW tasks)")
