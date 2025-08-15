"""Code Agent for code generation and GitHub repository review."""

import os
import tempfile
from pathlib import Path
from typing import List, Union
from urllib.parse import urlparse

import git
from pydantic_ai import Agent, RunContext

from ..config import MODEL_NAME
from ..models import (
    CodeAgentRequest,
    CodeAgentResult,
    CodeGenerationRequest,
    CodeGenerationResult,
    CodeIssue,
    CodeReviewRequest,
    CodeReviewResult,
    TaskType,
)


# System prompt for the code agent
CODE_SYSTEM_PROMPT = """
You are an expert Code Agent with deep expertise in software development, code generation, and code review.

Your capabilities:
1. Generate high-quality code based on descriptions and requirements
2. Review existing codebases and identify potential issues
3. Analyze GitHub repositories for code quality, best practices, and bugs
4. Provide detailed feedback with specific recommendations

Your tasks:
- For GENERATE tasks: Create clean, well-documented, production-ready code
- For REVIEW tasks: Analyze code for bugs, security issues, performance problems, and best practices

Guidelines for code generation:
- Write clean, readable, and maintainable code
- Include proper error handling and input validation
- Add comprehensive documentation and comments
- Follow language-specific best practices and conventions
- Consider edge cases and potential failure points

Guidelines for code review:
- Look for security vulnerabilities and potential exploits
- Check for performance bottlenecks and inefficiencies
- Verify proper error handling and edge case management
- Ensure code follows established patterns and conventions
- Identify potential bugs and logic errors
- Assess code maintainability and readability
- Check for proper testing coverage considerations

When reviewing code, categorize issues by severity:
- CRITICAL: Security vulnerabilities, data loss risks
- HIGH: Bugs that could cause system failures or data corruption
- MEDIUM: Performance issues, maintainability concerns
- LOW: Style issues, minor optimizations
"""


def clone_repository(github_url: str, branch: str = "main") -> str:
    """Clone a GitHub repository to a temporary directory.
    
    Args:
        github_url: The GitHub repository URL
        branch: Branch to clone (defaults to main)
        
    Returns:
        Path to the cloned repository
    """
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Clone the repository
        repo = git.Repo.clone_from(github_url, temp_dir)
        
        # Try to checkout the specified branch
        try:
            repo.git.checkout(branch)
        except git.exc.GitCommandError:
            # Branch doesn't exist, stay on default branch
            print(f"Branch '{branch}' not found, using default branch")
        
        return temp_dir
    except Exception as e:
        raise Exception(f"Failed to clone repository: {e}")


def analyze_repository_structure(repo_path: str) -> str:
    """Analyze the structure and content of a repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        Analysis summary as a string
    """
    try:
        repo_path = Path(repo_path)
        analysis = []
        
        # Get basic repository info
        analysis.append(f"Repository structure analysis for: {repo_path.name}")
        analysis.append("=" * 50)
        
        # Count files by extension
        file_counts = {}
        total_files = 0
        code_files = []
        
        for file_path in repo_path.rglob("*"):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                total_files += 1
                suffix = file_path.suffix.lower()
                file_counts[suffix] = file_counts.get(suffix, 0) + 1
                
                # Collect code files for detailed analysis
                if suffix in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.rb']:
                    code_files.append(file_path)
        
        analysis.append(f"Total files: {total_files}")
        analysis.append("File types:")
        for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                analysis.append(f"  {ext or '(no extension)'}: {count}")
        
        # Analyze key code files (sample up to 10)
        analysis.append("\nCode file analysis (sample):")
        for code_file in code_files[:10]:
            try:
                with open(code_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.splitlines())
                    analysis.append(f"  {code_file.relative_to(repo_path)}: {lines} lines")
            except Exception:
                analysis.append(f"  {code_file.relative_to(repo_path)}: (unable to read)")
        
        if len(code_files) > 10:
            analysis.append(f"  ... and {len(code_files) - 10} more code files")
        
        return "\n".join(analysis)
    except Exception as e:
        return f"Error analyzing repository: {e}"


def read_code_files(repo_path: str, max_files: int = 5) -> str:
    """Read the content of key code files for analysis.
    
    Args:
        repo_path: Path to the repository
        max_files: Maximum number of files to read
        
    Returns:
        Combined content of code files
    """
    try:
        repo_path = Path(repo_path)
        content_parts = []
        
        # Priority extensions for code analysis
        priority_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs']
        
        code_files = []
        for ext in priority_extensions:
            files = list(repo_path.rglob(f"*{ext}"))
            code_files.extend(files[:2])  # Take first 2 of each type
        
        # Limit total files
        code_files = code_files[:max_files]
        
        for code_file in code_files:
            try:
                with open(code_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Limit content size to avoid overwhelming the LLM
                    if len(content) > 5000:
                        content = content[:5000] + "\n... (truncated)"
                    
                    content_parts.append(f"""
File: {code_file.relative_to(repo_path)}
{'=' * 40}
{content}
{'=' * 40}
""")
            except Exception:
                content_parts.append(f"File: {code_file.relative_to(repo_path)} - (unable to read)")
        
        return "\n".join(content_parts) if content_parts else "No code files found or readable."
    except Exception as e:
        return f"Error reading code files: {e}"


# Create the code agent
code_agent = Agent(
    MODEL_NAME,
    system_prompt=CODE_SYSTEM_PROMPT,
    deps_type=RunContext,
)


@code_agent.tool
async def analyze_github_repository(ctx: RunContext, github_url: str, branch: str = "main") -> str:
    """Clone and analyze a GitHub repository.
    
    Args:
        ctx: The run context
        github_url: GitHub repository URL
        branch: Branch to analyze
        
    Returns:
        Repository analysis results
    """
    try:
        # Clone the repository
        repo_path = clone_repository(github_url, branch)
        
        # Get repository structure
        structure_analysis = analyze_repository_structure(repo_path)
        
        # Read key code files
        code_content = read_code_files(repo_path)
        
        return f"""
Repository Analysis:
{structure_analysis}

Key Code Files Content:
{code_content}
"""
    except Exception as e:
        return f"Error analyzing repository: {e}"


async def process_code_request(request: CodeAgentRequest) -> CodeAgentResult:
    """Process a code agent request (generation or review).
    
    Args:
        request: The code agent request
        
    Returns:
        Code agent result (generation or review)
    """
    if isinstance(request, CodeGenerationRequest):
        return await generate_code(request)
    elif isinstance(request, CodeReviewRequest):
        return await review_code(request)
    else:
        raise ValueError(f"Unknown request type: {type(request)}")


async def generate_code(request: CodeGenerationRequest) -> CodeGenerationResult:
    """Generate code based on the description.
    
    Args:
        request: Code generation request
        
    Returns:
        Generated code result
    """
    result = await code_agent.run(
        f"""Please generate code based on the following description:

Description: {request.code_description}

Requirements:
1. Generate clean, production-ready code
2. Include proper error handling and input validation
3. Add comprehensive documentation and comments
4. Follow best practices for the chosen language/framework
5. Consider edge cases and potential failure points
6. Make the code modular and maintainable

Please provide the complete code implementation."""
    )
    
    return CodeGenerationResult(
        generated_code=result.data if result.data else "Unable to generate code."
    )


async def review_code(request: CodeReviewRequest) -> CodeReviewResult:
    """Review code from a GitHub repository.
    
    Args:
        request: Code review request
        
    Returns:
        Code review result with summary and issues
    """
    github_url = str(request.github_url)
    branch = request.branch or "main"
    
    result = await code_agent.run(
        f"""Please review the code from this GitHub repository:

URL: {github_url}
Branch: {branch}

Use the analyze_github_repository tool to examine the codebase, then provide:

1. An overall review summary
2. Specific issues found, categorized by severity (CRITICAL, HIGH, MEDIUM, LOW)
3. Recommendations for improvement
4. Security considerations
5. Performance observations
6. Code quality assessment

Please be thorough in your analysis and provide actionable feedback."""
    )
    
    # Parse issues from the response (simplified approach)
    # In production, you'd want more sophisticated parsing
    issues = [
        CodeIssue(
            severity="MEDIUM",
            description="Automated code review completed. See summary for details.",
            file_path=None,
            line_number=None
        )
    ]
    
    return CodeReviewResult(
        review_summary=result.data if result.data else "Unable to complete code review.",
        issues=issues
    )


# Export the main functions
__all__ = ['process_code_request', 'generate_code', 'review_code', 'code_agent']
