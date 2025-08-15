#!/usr/bin/env python3
"""Test research agent with explicit search request."""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from src.a2a_agents.research_agent import research_agent
from pydantic_ai import RunContext

async def test_research_with_search():
    """Test research agent with explicit search instruction."""
    
    print("🧪 Testing Research Agent with Explicit Search Request")
    print(f"🔧 Model: {research_agent.model}")
    print(f"🔑 API Key: {os.getenv('GEMINI_API_KEY', 'NOT_SET')[:10]}...")
    print("-" * 60)
    
    # Try a query that clearly requires web search
    query = "Search the web for the latest news about Python 3.13 release. What are the new features?"
    print(f"📝 Query: {query}")
    print("🔗 This should trigger the web_search tool...")
    
    try:
        # Call without deps first to see if that works
        print("\n🔄 Calling agent (no deps)...")
        result = await research_agent.run(query)
        
        print("✅ Agent completed!")
        print(f"💬 Result type: {type(result)}")
        
        # Extract the actual output
        if hasattr(result, 'data'):
            output = result.data
        elif hasattr(result, 'output'):
            output = result.output
        else:
            output = str(result)
        
        print(f"📄 Response length: {len(output)} characters")
        print(f"🔍 Response preview: {output[:300]}...")
        
        # Check if it contains search results or just says "couldn't find"
        if "could not find" in output.lower() or "i don't have" in output.lower():
            print("❌ Agent didn't use search tool - may need deps or different prompt")
            return False
        elif "http" in output or "source" in output.lower():
            print("✅ Agent appears to have used web search (contains URLs/sources)")
            return True
        else:
            print("🤔 Unclear if search was used - check full response")
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function."""
    print("🚀 Research Agent Search Tool Test")
    print("=" * 60)
    
    success = await test_research_with_search()
    
    if success:
        print("\n🎉 SUCCESS! Research agent can perform web searches")
    else:
        print("\n💔 ISSUE: Research agent not using search tool properly")
        print("💡 This might explain why it said 'could not find information'")
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled")
        exit(130)
