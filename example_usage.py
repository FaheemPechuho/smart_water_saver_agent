"""
Example usage of the Smart Water Saver Agent API.
Demonstrates how to interact with the agent programmatically.
"""
import asyncio
import httpx
import json


async def test_agent():
    """Test the Smart Water Saver Agent endpoints."""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Smart Water Saver Agent - Example Usage")
    print("=" * 60)
    print()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: Health Check
        print("1. Testing /health endpoint...")
        print("-" * 60)
        try:
            response = await client.get(f"{base_url}/health")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print()
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure the agent is running: python main.py")
            return
        
        # Test 2: Watering Advice
        print("2. Testing Watering Advice Intent...")
        print("-" * 60)
        watering_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Should I water my garden today?"
                }
            ],
            "user_id": "example_user_123"
        }
        response = await client.post(f"{base_url}/smart-water-saver-agent", json=watering_request)
        print(f"Request: {watering_request['messages'][0]['content']}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test 3: Usage Query
        print("3. Testing Usage Query Intent...")
        print("-" * 60)
        usage_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "How much water did I use this week?"
                }
            ],
            "user_id": "example_user_123"
        }
        response = await client.post(f"{base_url}/smart-water-saver-agent", json=usage_request)
        print(f"Request: {usage_request['messages'][0]['content']}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test 4: Water Saving Tip
        print("4. Testing General Tip Intent...")
        print("-" * 60)
        tip_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Give me a water saving tip"
                }
            ],
            "user_id": "example_user_123"
        }
        response = await client.post(f"{base_url}/smart-water-saver-agent", json=tip_request)
        print(f"Request: {tip_request['messages'][0]['content']}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test 5: Multi-turn Conversation
        print("5. Testing Multi-turn Conversation...")
        print("-" * 60)
        conversation_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "Hello"
                },
                {
                    "role": "assistant",
                    "content": "Hi! How can I help you save water today?"
                },
                {
                    "role": "user",
                    "content": "What's the weather like for watering?"
                }
            ],
            "user_id": "example_user_123"
        }
        response = await client.post(f"{base_url}/smart-water-saver-agent", json=conversation_request)
        print(f"Conversation:")
        for msg in conversation_request['messages']:
            print(f"  {msg['role']}: {msg['content']}")
        print(f"\nResponse: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test 6: Fallback Handling
        print("6. Testing Fallback (Unknown Intent)...")
        print("-" * 60)
        unknown_request = {
            "messages": [
                {
                    "role": "user",
                    "content": "What's the meaning of life?"
                }
            ],
            "user_id": "example_user_123"
        }
        response = await client.post(f"{base_url}/smart-water-saver-agent", json=unknown_request)
        print(f"Request: {unknown_request['messages'][0]['content']}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)


def main():
    """Run the example usage."""
    print("\nStarting example usage tests...")
    print("Make sure the agent is running on http://localhost:8000")
    print()
    
    try:
        asyncio.run(test_agent())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n\nError running tests: {e}")


if __name__ == "__main__":
    main()

