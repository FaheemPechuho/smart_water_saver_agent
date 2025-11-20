"""
Quick verification script to check compliance with SPM Agents Format Guide Section F.
Run this after starting the server to verify all endpoints work correctly.
"""
import httpx
import json
import sys
from typing import Dict, Any


def print_result(test_name: str, passed: bool, details: str = ""):
    """Print test result with formatting."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"    {details}")


async def test_health_endpoint(base_url: str) -> bool:
    """Test the health check endpoint."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{base_url}/smart-water-saver-agent/health")
            
            if response.status_code != 200:
                print_result("Health Endpoint Status", False, f"Expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            # Check required fields
            checks = [
                ("status" in data, "Has 'status' field"),
                (data.get("status") == "ok", "Status is 'ok'"),
                ("agent_name" in data, "Has 'agent_name' field"),
                (data.get("agent_name") == "smart-water-saver-agent", "Agent name is correct"),
                ("ready" in data, "Has 'ready' field"),
            ]
            
            all_passed = all(check[0] for check in checks)
            if all_passed:
                print_result("Health Endpoint", True)
            else:
                failed = [check[1] for check in checks if not check[0]]
                print_result("Health Endpoint", False, f"Missing: {', '.join(failed)}")
            
            return all_passed
            
    except Exception as e:
        print_result("Health Endpoint", False, f"Error: {str(e)}")
        return False


async def test_agent_endpoint(base_url: str) -> bool:
    """Test the main agent endpoint."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            request_data = {
                "messages": [
                    {
                        "role": "user",
                        "content": "Should I water today?"
                    }
                ]
            }
            
            response = await client.post(
                f"{base_url}/smart-water-saver-agent",
                json=request_data
            )
            
            if response.status_code != 200:
                print_result("Agent Endpoint Status", False, f"Expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            # Check required fields
            checks = [
                ("agent_name" in data, "Has 'agent_name' field"),
                (data.get("agent_name") == "smart-water-saver-agent", "Agent name is 'smart-water-saver-agent'"),
                ("status" in data, "Has 'status' field"),
                (data.get("status") in ["success", "error"], "Status is 'success' or 'error'"),
                ("data" in data, "Has 'data' field"),
                ("error_message" in data, "Has 'error_message' field"),
            ]
            
            if data.get("status") == "success":
                checks.append((
                    data.get("data") is not None and "message" in data.get("data", {}),
                    "Data contains 'message' field"
                ))
            
            all_passed = all(check[0] for check in checks)
            if all_passed:
                print_result("Agent Endpoint", True)
            else:
                failed = [check[1] for check in checks if not check[0]]
                print_result("Agent Endpoint", False, f"Failed: {', '.join(failed)}")
            
            return all_passed
            
    except Exception as e:
        print_result("Agent Endpoint", False, f"Error: {str(e)}")
        return False


async def test_error_handling(base_url: str) -> bool:
    """Test error handling."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Send invalid request (empty messages)
            request_data = {
                "messages": []
            }
            
            response = await client.post(
                f"{base_url}/smart-water-saver-agent",
                json=request_data
            )
            
            # Should return error response, not crash
            if response.status_code >= 500:
                print_result("Error Handling", False, "Server crashed (500 error)")
                return False
            
            # Even on 4xx errors, should return JSON
            try:
                data = response.json()
                is_json = True
            except:
                is_json = False
            
            if not is_json:
                print_result("Error Handling", False, "Returned non-JSON response")
                return False
            
            print_result("Error Handling", True, "Returns JSON error responses")
            return True
            
    except Exception as e:
        print_result("Error Handling", False, f"Error: {str(e)}")
        return False


async def main():
    """Run all compliance tests."""
    print("=" * 60)
    print("SPM Agents Format Guide Section F - Compliance Verification")
    print("=" * 60)
    print()
    
    base_url = "http://localhost:8000"
    
    print(f"Testing against: {base_url}")
    print()
    
    results = []
    
    # Test 1: Health endpoint
    print("Test 1: Health Check Endpoint")
    results.append(await test_health_endpoint(base_url))
    print()
    
    # Test 2: Agent endpoint
    print("Test 2: Main Agent Endpoint")
    results.append(await test_agent_endpoint(base_url))
    print()
    
    # Test 3: Error handling
    print("Test 3: Error Handling")
    results.append(await test_error_handling(base_url))
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print()
        print("Your agent is COMPLIANT with SPM Agents Format Guide Section F!")
        print()
        print("Next steps:")
        print("1. Add your agent to the SPM-Agent-Registry (see AGENT_REGISTRY.md)")
        print("2. Deploy to production")
        print("3. Update registry with your deployment URL")
        return 0
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total} passed)")
        print()
        print("Please review the failed tests above and fix the issues.")
        return 1


if __name__ == "__main__":
    import asyncio
    sys.exit(asyncio.run(main()))

