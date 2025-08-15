#!/usr/bin/env python3
"""
Test all simple agents using Pydantic AI's native A2A support.
This demonstrates the clean, working solution!
"""

import asyncio
import json
import uuid
import requests
import time
from concurrent.futures import ThreadPoolExecutor


AGENTS = {
    "research": "http://localhost:8002",
    "code": "http://localhost:8003", 
    "data": "http://localhost:8004",
    "planning": "http://localhost:8005"
}

TEST_QUERIES = {
    "research": "What is artificial intelligence? One sentence.",
    "code": "Write a Python hello world function.",
    "data": "Convert this to JSON: name=John, age=30",
    "planning": "Plan a simple web app project in 3 steps."
}


def test_agent(agent_name: str, base_url: str, query: str) -> dict:
    """Test a single agent with proper A2A protocol."""
    
    a2a_request = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "kind": "message", 
                "messageId": str(uuid.uuid4()),
                "parts": [{"kind": "text", "text": query}]
            }
        },
        "id": str(uuid.uuid4())
    }
    
    try:
        print(f"🧪 Testing {agent_name} agent...")
        start_time = time.time()
        
        response = requests.post(
            f"{base_url}/",
            json=a2a_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {agent_name} agent: SUCCESS in {elapsed:.1f}s")
            return {
                "agent": agent_name,
                "status": "success",
                "elapsed": elapsed,
                "response": data
            }
        else:
            print(f"❌ {agent_name} agent: HTTP {response.status_code}")
            return {
                "agent": agent_name,
                "status": "error",
                "error": f"HTTP {response.status_code}: {response.text}"
            }
            
    except Exception as e:
        print(f"💥 {agent_name} agent: {str(e)}")
        return {
            "agent": agent_name,
            "status": "error", 
            "error": str(e)
        }


def test_connectivity():
    """Test basic connectivity to all agents."""
    print("🔍 Testing Agent Connectivity")
    print("-" * 40)
    
    for agent_name, base_url in AGENTS.items():
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code in [200, 405]:  # 405 Method Not Allowed is expected
                print(f"✅ {agent_name}: Reachable")
            else:
                print(f"❌ {agent_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"💥 {agent_name}: {str(e)}")
    print()


def test_a2a_protocol():
    """Test A2A protocol with all agents."""
    print("🧪 Testing A2A Protocol")
    print("-" * 40)
    
    results = []
    
    # Test agents in parallel for efficiency
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for agent_name, base_url in AGENTS.items():
            query = TEST_QUERIES[agent_name]
            future = executor.submit(test_agent, agent_name, base_url, query)
            futures.append(future)
        
        for future in futures:
            result = future.result()
            results.append(result)
    
    return results


def main():
    """Main test function."""
    print("🚀 Testing All Simple A2A Agents")
    print("Using Pydantic AI's native A2A support - no FastA2A!")
    print("=" * 60)
    
    # Test connectivity first
    test_connectivity()
    
    # Test A2A protocol
    results = test_a2a_protocol()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "error"]
    
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        avg_time = sum(r["elapsed"] for r in successful) / len(successful)
        print(f"⏱️  Average response time: {avg_time:.1f}s")
    
    if failed:
        print(f"\n💔 Failed agents:")
        for result in failed:
            print(f"  • {result['agent']}: {result.get('error', 'Unknown error')}")
    
    # Save results
    with open("simple_agents_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Results saved to: simple_agents_test_results.json")
    
    return len(failed) == 0


if __name__ == "__main__":
    try:
        success = main()
        print(f"\n🎯 Overall result: {'SUCCESS' if success else 'PARTIAL SUCCESS'}")
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled")
        exit(130)
