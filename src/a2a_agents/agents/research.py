"""Research Agent for web search and information synthesis."""

import os
from typing import List
from urllib.parse import urlparse

from duckduckgo_search import DDGS
from pydantic import HttpUrl
from pydantic_ai import Agent, RunContext

from ..config import MODEL_NAME
from ..models import ResearchQuery, ResearchResult


# System prompt for the research agent
RESEARCH_SYSTEM_PROMPT = """
You are a highly skilled Research Agent specializing in web search and information synthesis.

Your capabilities:
1. Search the web for relevant information using DuckDuckGo
2. Analyze and synthesize information from multiple sources
3. Provide accurate, well-structured summaries
4. Cite all sources used in your research

Your tasks:
1. When given a query, search for comprehensive information
2. Evaluate source credibility and relevance
3. Synthesize findings into a coherent, informative summary
4. Always include the source URLs you used

Guidelines:
- Be thorough but concise in your summaries
- Focus on factual, verifiable information
- If information is conflicting between sources, note this
- Prioritize recent and authoritative sources
- Always maintain objectivity and avoid bias
"""


def search_web(query: str, max_results: int = 10) -> List[dict]:
    """Search the web using DuckDuckGo and return results.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of search results with title, body, and href
    """
    import time
    
    # Try multiple times with different approaches
    for attempt in range(3):
        try:
            print(f"Search attempt {attempt + 1} for query: {query}")
            with DDGS() as ddgs:
                results = []
                search_iter = ddgs.text(query, max_results=max_results)
                
                for result in search_iter:
                    if result:  # Make sure result is not None
                        results.append({
                            'title': result.get('title', 'No title'),
                            'body': result.get('body', 'No content'),
                            'href': result.get('href', 'No URL')
                        })
                
                if results:
                    print(f"Search successful: found {len(results)} results")
                    return results
                else:
                    print(f"Search attempt {attempt + 1}: No results found")
                    
        except Exception as e:
            print(f"Search attempt {attempt + 1} failed: {e}")
            if attempt < 2:  # Don't sleep on last attempt
                time.sleep(1)  # Brief pause between attempts
    
    print("All search attempts failed")
    return []


def validate_url(url_string: str) -> bool:
    """Validate if a string is a proper URL."""
    try:
        result = urlparse(url_string)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


# Create the research agent with better configuration
research_agent = Agent(
    model=MODEL_NAME,
    name="Research Agent",
    system_prompt=RESEARCH_SYSTEM_PROMPT,
    deps_type=RunContext,
    retries=2,
)


@research_agent.tool
async def web_search(ctx: RunContext, query: str, max_results: int = 8) -> str:
    """Search the web for information related to the query.
    
    Args:
        ctx: The run context
        query: Search query string
        max_results: Maximum number of results to fetch
        
    Returns:
        Formatted search results as a string
    """
    search_results = search_web(query, max_results)
    
    if not search_results:
        return "No search results found for the query."
    
    formatted_results = []
    for i, result in enumerate(search_results, 1):
        formatted_result = f"""
Result {i}:
Title: {result['title']}
URL: {result['href']}
Content: {result['body']}
---
"""
        formatted_results.append(formatted_result)
    
    return "\n".join(formatted_results)


async def research_query(query: ResearchQuery) -> ResearchResult:
    """Process a research query and return synthesized results.
    
    Args:
        query: The research query input
        
    Returns:
        Research results with summary and source URLs
    """
    try:
        # Run the agent with the query
        result = await research_agent.run(
            f"""Please research the following query: "{query.query}"

Instructions:
1. Use the web_search tool to find relevant information
2. Analyze the search results carefully
3. Provide a comprehensive summary of your findings
4. List all the source URLs you used in your research

Your response should be well-structured and informative."""
        )
    except Exception as e:
        # Graceful degradation if agent fails
        print(f"Research agent error: {e}")
        return ResearchResult(
            summary=f"Unable to complete research for query: '{query.query}'. Error: {str(e)}",
            source_urls=[]
        )
    
    # Extract source URLs from the agent's context
    # This is a simplified approach - in production, you'd want more sophisticated URL extraction
    search_results = search_web(query.query, max_results=6)
    source_urls = []
    
    for result_item in search_results:
        url = result_item.get('href', '')
        if validate_url(url):
            try:
                source_urls.append(HttpUrl(url))
            except Exception:
                continue  # Skip invalid URLs
    
    # Ensure we have at least some sources, even if search failed
    if not source_urls and search_results:
        # Try to extract any valid URLs from search results
        for result_item in search_results:
            url = result_item.get('href', '')
            if url and url.startswith(('http://', 'https://')):
                try:
                    source_urls.append(HttpUrl(url))
                except Exception:
                    continue
    
    return ResearchResult(
        summary=result.data if result.data else "Unable to generate research summary.",
        source_urls=source_urls[:6]  # Limit to 6 sources for manageable output
    )


# Export the main function for the agent
__all__ = ['research_query', 'research_agent']
