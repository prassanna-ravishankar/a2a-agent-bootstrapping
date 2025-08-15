#!/usr/bin/env python3
"""Test the agent directly without A2A protocol."""

import asyncio
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import our agent directly
from a2a_agents.agents.research import research_agent
from pydantic_ai import RunContext


async def test_direct_agent():
    """Test the research agent directly without A2A protocol."""
    
    print("🧪 Testing Research Agent Directly")
    print(f"🔧 Model: {research_agent.model}")
    print(f"🔑 API Key: {os.getenv('GEMINI_API_KEY', 'NOT_SET')[:10]}...")
    print("-" * 50)
    
    try:
        # Test query
        query = "What is Python programming language? Keep it brief."
        print(f"📝 Query: {query}")
        print("🔗 Calling agent directly...")
        
        # Call the agent without deps for simple test
        result = await research_agent.run(query)
        
        print("✅ SUCCESS! Agent responded:")
        print(f"💬 {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    print("🚀 Direct Agent Test (No A2A)")
    print("=" * 50)
    
    success = await test_direct_agent()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS! Agent working directly")
        print("💡 Issue might be in A2A protocol layer")
    else:
        print("💔 FAILED! Check API key and agent configuration")
    
    return success


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled")
        exit(130)
