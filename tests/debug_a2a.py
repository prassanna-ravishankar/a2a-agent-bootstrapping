#!/usr/bin/env python3
"""
Enhanced A2A debugging with comprehensive logging and timeout handling.
Implements best practices from web search results.
"""

import asyncio
import json
import time
import uuid
import logging
from typing import Optional
import requests

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class A2ADebugger:
    """Enhanced A2A client with debugging and resilience features."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.agents = {
            "research": f"{base_url}/research",
            "code": f"{base_url}/code", 
            "data": f"{base_url}/data",
            "planning": f"{base_url}/planning"
        }
    
    def create_a2a_request(self, message: str) -> dict:
        """Create a properly formatted A2A JSON-RPC request."""
        request_id = str(uuid.uuid4())
        message_id = str(uuid.uuid4())
        
        return {
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
    
    def test_with_retry_and_backoff(self, agent_name: str, message: str, max_retries: int = 3) -> dict:
        """
        Test agent with retry logic and exponential backoff.
        Implements strategy #1 from web search results.
        """
        agent_url = self.agents.get(agent_name)
        if not agent_url:
            return {"error": f"Unknown agent: {agent_name}"}
        
        a2a_request = self.create_a2a_request(message)
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries} for {agent_name} agent")
                
                # Implement progressive timeout strategy (#2 from web search)
                timeout = 30 + (attempt * 30)  # 30s, 60s, 90s
                logger.info(f"Using timeout: {timeout}s")
                
                start_time = time.time()
                
                response = requests.post(
                    f"{agent_url}/",
                    json=a2a_request,
                    headers={"Content-Type": "application/json"},
                    timeout=timeout,
                    # Add connection timeout separately
                    stream=False  # Don't stream to avoid hanging
                )
                
                elapsed = time.time() - start_time
                logger.info(f"Request completed in {elapsed:.2f}s with status {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Success! Response keys: {list(data.keys())}")
                    return {
                        "agent": agent_name,
                        "url": agent_url,
                        "message": message,
                        "response": data.get("result", data),
                        "status": "success",
                        "elapsed_time": elapsed,
                        "attempt": attempt + 1
                    }
                elif response.status_code >= 500:
                    # Server error - retry with backoff
                    logger.warning(f"Server error {response.status_code}, will retry after backoff")
                    if attempt < max_retries - 1:
                        backoff_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                        logger.info(f"Backing off for {backoff_time}s")
                        time.sleep(backoff_time)
                        continue
                else:
                    # Client error - don't retry
                    logger.error(f"Client error {response.status_code}: {response.text}")
                    return {
                        "agent": agent_name,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "status": "client_error",
                        "attempt": attempt + 1
                    }
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout after {timeout}s on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    backoff_time = 2 ** attempt
                    logger.info(f"Timeout backoff for {backoff_time}s")
                    time.sleep(backoff_time)
                    continue
                else:
                    return {
                        "agent": agent_name,
                        "error": f"Timeout after {max_retries} attempts",
                        "status": "timeout",
                        "attempt": attempt + 1
                    }
                    
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Connection error: {str(e)}")
                return {
                    "agent": agent_name,
                    "error": f"Connection error: {str(e)}",
                    "status": "connection_error",
                    "attempt": attempt + 1
                }
                
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return {
                    "agent": agent_name,
                    "error": f"Unexpected error: {str(e)}",
                    "status": "error",
                    "attempt": attempt + 1
                }
        
        return {
            "agent": agent_name,
            "error": "All retry attempts failed",
            "status": "failed",
            "attempts": max_retries
        }
    
    def test_health_and_connectivity(self) -> dict:
        """
        Test basic server connectivity before A2A tests.
        Implements observability strategy (#3 from web search).
        """
        logger.info("Testing server health and connectivity...")
        
        try:
            # Test health endpoint
            start_time = time.time()
            health_response = requests.get(f"{self.base_url}/health", timeout=10)
            health_time = time.time() - start_time
            
            logger.info(f"Health check: {health_response.status_code} in {health_time:.2f}s")
            
            # Test A2A endpoint connectivity (expect validation error)
            start_time = time.time()
            connectivity_response = requests.post(
                f"{self.base_url}/research/",
                json={"test": "connectivity"},
                timeout=10
            )
            connectivity_time = time.time() - start_time
            
            logger.info(f"A2A connectivity: {connectivity_response.status_code} in {connectivity_time:.2f}s")
            
            return {
                "health": {
                    "status_code": health_response.status_code,
                    "response_time": health_time,
                    "working": health_response.status_code == 200
                },
                "a2a_connectivity": {
                    "status_code": connectivity_response.status_code,
                    "response_time": connectivity_time,
                    "reachable": connectivity_response.status_code in [400, 422, 500]  # Any response means reachable
                }
            }
            
        except Exception as e:
            logger.error(f"Connectivity test failed: {str(e)}")
            return {
                "error": str(e),
                "health": {"working": False},
                "a2a_connectivity": {"reachable": False}
            }


def main():
    """
    Main debugging function implementing multiple strategies from web search.
    """
    print("🔍 Enhanced A2A Debugging Session")
    print("📊 Implementing timeout handling and observability best practices")
    print("=" * 70)
    
    debugger = A2ADebugger()
    
    # Strategy #3: Enhanced Observability
    print("\n🏥 Step 1: Testing Server Health & Connectivity")
    print("-" * 50)
    connectivity = debugger.test_health_and_connectivity()
    
    if connectivity.get("health", {}).get("working"):
        print("✅ Server health check: OK")
    else:
        print("❌ Server health check: FAILED")
        return False
    
    if connectivity.get("a2a_connectivity", {}).get("reachable"):
        print("✅ A2A endpoints: Reachable")
    else:
        print("❌ A2A endpoints: Unreachable")
        return False
    
    # Strategy #1 & #2: Retry logic with progressive timeouts
    print("\n🧪 Step 2: Testing A2A Agent with Retry Logic")
    print("-" * 50)
    
    test_message = "What is Python programming? Be very brief - one sentence only."
    
    logger.info(f"Testing research agent with message: {test_message}")
    result = debugger.test_with_retry_and_backoff("research", test_message)
    
    print(f"\n📋 Final Result:")
    print(f"Status: {result.get('status', 'unknown')}")
    
    if result.get("status") == "success":
        print(f"✅ SUCCESS! Agent responded in {result.get('elapsed_time', 0):.1f}s")
        print(f"🔄 Succeeded on attempt: {result.get('attempt', 1)}")
        response = result.get("response", "")
        if isinstance(response, dict) and "result" in response:
            response = response["result"]
        print(f"💬 Response: {str(response)[:200]}...")
        return True
    else:
        print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        print(f"🔄 Final attempt: {result.get('attempt', 1)}")
        return False


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Debugging session cancelled")
        exit(130)
