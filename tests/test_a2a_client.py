#!/usr/bin/env python3
"""
A2A Client Test Script

This script demonstrates how to interact with our A2A agents using HTTP requests
with proper A2A protocol formatting. It tests all 4 agents: Research, Code, 
Data Transformation, and Planning.
"""

import asyncio
import json
import sys
from typing import Dict, List
import uuid

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class A2AAgentTester:
    """Test client for A2A Agent Bootstrapping."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.agents = {
            "research": f"{base_url}/research",
            "code": f"{base_url}/code", 
            "data": f"{base_url}/data",
            "planning": f"{base_url}/planning"
        }
    
    async def test_agent(self, agent_name: str, message: str) -> Dict:
        """Test a specific agent with a message using proper A2A protocol."""
        agent_url = self.agents.get(agent_name)
        if not agent_url:
            return {"error": f"Unknown agent: {agent_name}"}
        
        # Create proper A2A JSON-RPC request
        request_id = str(uuid.uuid4())
        message_id = str(uuid.uuid4())
        
        a2a_request = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "kind": "message",
                    "messageId": message_id,
                    "parts": [
                        {
                            "kind": "text",
                            "text": message
                        }
                    ]
                }
            },
            "id": request_id
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                print(f"🔗 Sending A2A request to {agent_name} agent at {agent_url}")
                print(f"📝 Message: {message[:100]}{'...' if len(message) > 100 else ''}")
                
                response = await client.post(
                    agent_url + "/",
                    json=a2a_request,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    if "result" in response_data:
                        result_content = response_data["result"]
                        print(f"✅ Success! Response from {agent_name} agent")
                        return {
                            "agent": agent_name,
                            "url": agent_url,
                            "message": message,
                            "response": result_content,
                            "status": "success",
                            "request_id": request_id
                        }
                    else:
                        error_msg = response_data.get("error", "Unknown error in response")
                        print(f"❌ A2A Error from {agent_name} agent: {error_msg}")
                        return {
                            "agent": agent_name,
                            "url": agent_url,
                            "message": message,
                            "error": f"A2A Error: {error_msg}",
                            "status": "error"
                        }
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    print(f"❌ HTTP Error from {agent_name} agent: {error_msg}")
                    return {
                        "agent": agent_name,
                        "url": agent_url,
                        "message": message,
                        "error": error_msg,
                        "status": "error"
                    }
                
        except Exception as e:
            print(f"❌ Error testing {agent_name} agent: {str(e)}")
            return {
                "agent": agent_name,
                "url": agent_url,
                "message": message,
                "error": str(e),
                "status": "error"
            }
    
    async def test_all_agents(self) -> List[Dict]:
        """Test all agents with different queries."""
        test_cases = [
            {
                "agent": "research",
                "message": "What are the latest developments in quantum computing in 2024?"
            },
            {
                "agent": "code", 
                "message": "Generate a Python function to calculate the Fibonacci sequence efficiently using memoization."
            },
            {
                "agent": "data",
                "message": "Convert this CSV data to JSON: name,age,city\\nAlice,25,New York\\nBob,30,London\\nCharlie,35,Tokyo"
            },
            {
                "agent": "planning",
                "message": "Create a plan for launching a mobile app for task management."
            }
        ]
        
        results = []
        
        print("🚀 Testing A2A Agent Bootstrapping with real queries...")
        print("=" * 60)
        
        for test_case in test_cases:
            agent_name = test_case["agent"]
            message = test_case["message"]
            
            print(f"\n🧪 Testing {agent_name.title()} Agent")
            print(f"📝 Query: {message}")
            print("-" * 40)
            
            result = await self.test_agent(agent_name, message)
            results.append(result)
            
            if result["status"] == "success":
                print(f"💬 Response: {result['response']}")
            else:
                print(f"💥 Error: {result['error']}")
            
            print("-" * 40)
        
        return results
    
    async def check_agent_cards(self) -> Dict:
        """Check all agent cards for A2A discovery."""
        import httpx
        
        print("\n🔍 Checking A2A Agent Cards...")
        print("=" * 40)
        
        agent_cards = {}
        
        async with httpx.AsyncClient() as client:
            for agent_name, agent_url in self.agents.items():
                card_url = f"{agent_url}/.well-known/agent.json"
                try:
                    response = await client.get(card_url)
                    if response.status_code == 200:
                        card_data = response.json()
                        agent_cards[agent_name] = card_data
                        print(f"✅ {agent_name.title()} Agent Card: {card_data.get('name', 'Unknown')}")
                        print(f"   🔗 URL: {card_data.get('url', 'N/A')}")
                        print(f"   📋 Skills: {[skill.get('name', 'N/A') for skill in card_data.get('skills', [])]}")
                    else:
                        print(f"❌ {agent_name.title()} Agent Card: HTTP {response.status_code}")
                        agent_cards[agent_name] = {"error": f"HTTP {response.status_code}"}
                except Exception as e:
                    print(f"💥 {agent_name.title()} Agent Card Error: {str(e)}")
                    agent_cards[agent_name] = {"error": str(e)}
        
        return agent_cards


async def main():
    """Main test function."""
    print("🤖 A2A Agent Bootstrapping - Client Test")
    print("🔧 Using gemini-2.5-flash-lite model")
    print("=" * 60)
    
    # Initialize tester
    tester = A2AAgentTester()
    
    # Check agent cards first
    agent_cards = await tester.check_agent_cards()
    
    # Test all agents
    results = await tester.test_all_agents()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    
    successful_tests = [r for r in results if r["status"] == "success"]
    failed_tests = [r for r in results if r["status"] == "error"]
    
    print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed tests: {len(failed_tests)}/{len(results)}")
    
    if failed_tests:
        print("\n💥 Failed Tests:")
        for test in failed_tests:
            print(f"  • {test['agent']}: {test['error']}")
    
    # Save results
    output_file = "a2a_test_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "agent_cards": agent_cards,
            "test_results": results,
            "summary": {
                "total_tests": len(results),
                "successful": len(successful_tests),
                "failed": len(failed_tests)
            }
        }, f, indent=2)
    
    print(f"\n📄 Results saved to: {output_file}")
    
    return len(failed_tests) == 0


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)
