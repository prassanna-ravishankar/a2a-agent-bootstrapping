"""Logic and Planning Agent for breaking down high-level goals into actionable steps."""

import re
from typing import List

from pydantic_ai import Agent, RunContext

from .config import MODEL_NAME
from .models import PlanningRequest, PlanningResult


# System prompt for the planning agent
PLANNING_SYSTEM_PROMPT = """
You are an expert Logic and Planning Agent specializing in strategic thinking, goal decomposition, and project planning.

Your capabilities:
1. Analyze complex, high-level goals and objectives
2. Break down goals into logical, sequential, actionable steps
3. Identify dependencies and prerequisites between tasks
4. Consider resource requirements and constraints
5. Create realistic timelines and milestones
6. Account for potential risks and contingencies
7. Ensure plans are specific, measurable, and achievable

Your approach to planning:
1. **Goal Analysis**: Understand the full scope and context of the goal
2. **Decomposition**: Break complex goals into smaller, manageable components
3. **Sequencing**: Order tasks logically based on dependencies and prerequisites
4. **Specificity**: Make each step concrete and actionable
5. **Validation**: Ensure the plan is comprehensive and realistic

Guidelines for creating plans:
- Start with high-level phases, then break into detailed steps
- Each step should be specific and actionable (start with action verbs)
- Consider dependencies - what must be completed before each step
- Include verification/validation steps where appropriate
- Account for testing, review, and iteration phases
- Consider resource requirements (time, tools, skills, budget)
- Include risk mitigation and contingency planning
- Make steps measurable with clear success criteria

Step formatting requirements:
- Use clear, action-oriented language
- Start each step with an action verb (Create, Develop, Test, Deploy, etc.)
- Be specific about deliverables and outcomes
- Include relevant details without being overly verbose
- Consider both technical and non-technical aspects
- Account for communication and coordination needs

Types of goals you excel at planning:
- Software development projects
- Business initiatives and strategies
- Research and analysis projects
- Learning and skill development
- Process improvement initiatives
- Product launches and marketing campaigns
- Personal productivity and life goals
- Event planning and project management
"""


def analyze_goal_complexity(goal: str) -> str:
    """Analyze the complexity and characteristics of a goal.
    
    Args:
        goal: The goal string to analyze
        
    Returns:
        Analysis summary as a string
    """
    analysis_points = []
    
    # Basic length and complexity indicators
    word_count = len(goal.split())
    analysis_points.append(f"Word count: {word_count}")
    
    if word_count < 10:
        complexity = "Simple"
    elif word_count < 25:
        complexity = "Moderate"
    else:
        complexity = "Complex"
    
    analysis_points.append(f"Complexity level: {complexity}")
    
    # Look for key indicators
    indicators = {
        "technical": ["develop", "build", "code", "implement", "deploy", "system", "software", "app"],
        "business": ["launch", "market", "revenue", "customer", "business", "strategy", "sales"],
        "research": ["research", "analyze", "study", "investigate", "explore", "understand"],
        "learning": ["learn", "master", "improve", "skill", "knowledge", "education", "training"],
        "creative": ["design", "create", "write", "produce", "craft", "artistic", "creative"],
        "process": ["improve", "optimize", "streamline", "process", "workflow", "efficiency"]
    }
    
    detected_categories = []
    goal_lower = goal.lower()
    
    for category, keywords in indicators.items():
        if any(keyword in goal_lower for keyword in keywords):
            detected_categories.append(category)
    
    if detected_categories:
        analysis_points.append(f"Detected categories: {', '.join(detected_categories)}")
    
    # Time indicators
    time_keywords = ["urgent", "asap", "quickly", "immediately", "long-term", "future", "eventually"]
    if any(keyword in goal_lower for keyword in time_keywords):
        analysis_points.append("Time sensitivity detected")
    
    return " | ".join(analysis_points)


def extract_steps_from_text(text: str) -> List[str]:
    """Extract step items from AI-generated text.
    
    Args:
        text: Text containing steps or plan
        
    Returns:
        List of extracted steps
    """
    steps = []
    
    # Look for numbered lists
    numbered_pattern = r'^\d+\.\s*(.+)$'
    bullet_pattern = r'^[-*•]\s*(.+)$'
    
    lines = text.split('\n')
    current_step = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for numbered items
        numbered_match = re.match(numbered_pattern, line)
        if numbered_match:
            if current_step:
                steps.append(current_step.strip())
            current_step = numbered_match.group(1)
            continue
        
        # Check for bullet items
        bullet_match = re.match(bullet_pattern, line)
        if bullet_match:
            if current_step:
                steps.append(current_step.strip())
            current_step = bullet_match.group(1)
            continue
        
        # Check if line looks like a step (starts with action verb)
        action_verbs = [
            'create', 'develop', 'build', 'design', 'implement', 'test', 'deploy',
            'analyze', 'research', 'study', 'plan', 'organize', 'prepare',
            'write', 'document', 'review', 'validate', 'verify', 'establish',
            'configure', 'install', 'setup', 'initialize', 'launch', 'publish',
            'gather', 'collect', 'identify', 'define', 'specify', 'determine'
        ]
        
        first_word = line.split()[0].lower() if line.split() else ""
        if any(first_word.startswith(verb) for verb in action_verbs):
            if current_step:
                steps.append(current_step.strip())
            current_step = line
            continue
        
        # Continue current step if we're in one
        if current_step:
            current_step += " " + line
    
    # Add the last step
    if current_step:
        steps.append(current_step.strip())
    
    # Fallback: split by sentences if no clear steps found
    if not steps and text:
        sentences = re.split(r'[.!?]+', text)
        steps = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    return steps[:20]  # Limit to 20 steps for manageable output


def validate_and_improve_steps(steps: List[str]) -> List[str]:
    """Validate and improve the quality of steps.
    
    Args:
        steps: List of raw steps
        
    Returns:
        Improved list of steps
    """
    improved_steps = []
    
    for step in steps:
        if not step or len(step.strip()) < 5:
            continue
        
        # Clean up the step
        step = step.strip()
        
        # Remove leading numbers or bullets if they exist
        step = re.sub(r'^[\d\.\-\*•\s]+', '', step).strip()
        
        # Ensure step starts with capital letter
        if step and step[0].islower():
            step = step[0].upper() + step[1:]
        
        # Ensure step ends with period if it's a sentence
        if step and not step.endswith(('.', '!', '?', ':')):
            step += '.'
        
        # Skip if too short or not actionable
        if len(step) < 10:
            continue
        
        improved_steps.append(step)
    
    return improved_steps


# Create the planning agent
planning_agent = Agent(
    MODEL_NAME,
    system_prompt=PLANNING_SYSTEM_PROMPT,
    deps_type=RunContext,
)


@planning_agent.tool
async def analyze_goal_context(ctx: RunContext, goal: str) -> str:
    """Analyze the goal to understand its context and requirements.
    
    Args:
        ctx: The run context
        goal: The goal to analyze
        
    Returns:
        Analysis of the goal's context and requirements
    """
    complexity_analysis = analyze_goal_complexity(goal)
    
    return f"""
Goal Analysis:
{complexity_analysis}

Goal: "{goal}"

This analysis will help in creating a comprehensive and realistic plan.
"""


async def create_plan(request: PlanningRequest) -> PlanningResult:
    """Create a detailed plan for achieving the specified goal.
    
    Args:
        request: Planning request with the goal
        
    Returns:
        Planning result with sequential steps
    """
    goal = request.goal
    
    # Use the planning agent to create a comprehensive plan
    result = await planning_agent.run(
        f"""Please create a detailed, actionable plan to achieve the following goal:

Goal: "{goal}"

Instructions:
1. Use the analyze_goal_context tool to understand the goal's requirements
2. Break down the goal into logical phases and sequential steps
3. Make each step specific, actionable, and measurable
4. Consider dependencies, prerequisites, and logical ordering
5. Include validation and review steps where appropriate
6. Account for potential challenges and mitigation strategies

Format your response as a numbered list of specific, actionable steps. Each step should:
- Start with an action verb (Create, Develop, Test, etc.)
- Be specific about what needs to be accomplished
- Include relevant details without being overly verbose
- Consider both technical and non-technical aspects

Provide a comprehensive plan that someone could follow to achieve this goal."""
    )
    
    # Extract steps from the AI response
    ai_response = result.data if result.data else ""
    extracted_steps = extract_steps_from_text(ai_response)
    
    # Improve and validate the steps
    final_steps = validate_and_improve_steps(extracted_steps)
    
    # Ensure we have at least some basic steps even if extraction failed
    if not final_steps:
        # Create fallback basic steps
        final_steps = [
            f"Define and clarify the specific requirements for: {goal}",
            f"Research best practices and approaches for achieving: {goal}",
            f"Create a detailed implementation plan for: {goal}",
            f"Execute the plan with regular progress monitoring",
            f"Review and validate the results against the original goal"
        ]
    
    return PlanningResult(steps=final_steps)


# Export the main function
__all__ = ['create_plan', 'planning_agent']
