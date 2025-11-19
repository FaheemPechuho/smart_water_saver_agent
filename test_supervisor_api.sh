#!/bin/bash
# Smart Water Saver Agent - Supervisor API Test Script (Linux/Mac)
# Run this script to test all endpoints before sharing with supervisor

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Smart Water Saver Agent - API Testing Suite         ║"
echo "║  Testing Supervisor-Worker API Contract              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

BASE_URL="http://localhost:8000"
TESTS_PASSED=0
TESTS_FAILED=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=$3
    local body=$4
    
    echo -e "${YELLOW}Testing: $name${NC}"
    echo -e "${CYAN}URL: $url${NC}"
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$url" -H "Content-Type: application/json" -d "$body")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body_response=$(echo "$response" | sed '$d')
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✅ Status Code: $http_code${NC}"
        
        # Check if response follows AgentResponse format
        agent_name=$(echo "$body_response" | jq -r '.agent_name // empty')
        status=$(echo "$body_response" | jq -r '.status // empty')
        
        if [ ! -z "$agent_name" ] && [ ! -z "$status" ]; then
            echo -e "${GREEN}✅ Response Format: Valid AgentResponse${NC}"
            echo -e "   Agent: $agent_name"
            echo -e "   Status: $status"
            
            content=$(echo "$body_response" | jq -r '.data.content // empty' | head -c 80)
            if [ ! -z "$content" ]; then
                echo -e "   Response: $content..."
            fi
        else
            echo -e "${YELLOW}⚠️  Warning: Response may not follow AgentResponse format${NC}"
        fi
        
        echo ""
        return 0
    else
        echo -e "${RED}❌ FAILED: HTTP $http_code${NC}"
        echo "$body_response"
        echo ""
        return 1
    fi
}

echo "Starting tests against: $BASE_URL"
echo "Make sure the server is running (python main.py)"
echo ""
sleep 2

# Test 1: Health Check
echo "═══════════════════════════════════════════════════════"
echo "TEST 1: Health Check Endpoint"
echo "═══════════════════════════════════════════════════════"
if test_endpoint "Health Check" "$BASE_URL/health" "GET"; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Test 2: Root Endpoint
echo "═══════════════════════════════════════════════════════"
echo "TEST 2: Root Endpoint"
echo "═══════════════════════════════════════════════════════"
if test_endpoint "Root" "$BASE_URL/" "GET"; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Test 3: Chat - Watering Advice
echo "═══════════════════════════════════════════════════════"
echo "TEST 3: Chat - Watering Advice"
echo "═══════════════════════════════════════════════════════"
BODY='{"messages":[{"role":"user","content":"Should I water my garden today?"}],"user_id":"test_user_001"}'
if test_endpoint "Watering Advice" "$BASE_URL/chat" "POST" "$BODY"; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Test 4: Chat - Usage Query
echo "═══════════════════════════════════════════════════════"
echo "TEST 4: Chat - Usage Query"
echo "═══════════════════════════════════════════════════════"
BODY='{"messages":[{"role":"user","content":"How much water did I use this week?"}],"user_id":"test_user_001"}'
if test_endpoint "Usage Query" "$BASE_URL/chat" "POST" "$BODY"; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Test 5: Chat - Water Saving Tip
echo "═══════════════════════════════════════════════════════"
echo "TEST 5: Chat - Water Saving Tip"
echo "═══════════════════════════════════════════════════════"
BODY='{"messages":[{"role":"user","content":"Give me a water saving tip"}],"user_id":"test_user_001"}'
if test_endpoint "Water Saving Tip" "$BASE_URL/chat" "POST" "$BODY"; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Test 6: Chat - Without User ID
echo "═══════════════════════════════════════════════════════"
echo "TEST 6: Chat - Anonymous Request (No User ID)"
echo "═══════════════════════════════════════════════════════"
BODY='{"messages":[{"role":"user","content":"What are the best times to water plants?"}]}'
if test_endpoint "Anonymous Chat" "$BASE_URL/chat" "POST" "$BODY"; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Test 7: Chat - Multi-turn Conversation
echo "═══════════════════════════════════════════════════════"
echo "TEST 7: Chat - Multi-turn Conversation"
echo "═══════════════════════════════════════════════════════"
BODY='{"messages":[{"role":"user","content":"What is the weather like?"},{"role":"assistant","content":"The weather is partly cloudy."},{"role":"user","content":"Should I water based on that?"}],"user_id":"test_user_001"}'
if test_endpoint "Multi-turn Conversation" "$BASE_URL/chat" "POST" "$BODY"; then
    ((TESTS_PASSED++))
else
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                    TEST SUMMARY                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ Tests Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}❌ Tests Failed: $TESTS_FAILED${NC}"
else
    echo -e "${RED}❌ Tests Failed: $TESTS_FAILED${NC}"
fi
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! Agent is ready for supervisor integration.${NC}"
    echo ""
    echo -e "${CYAN}Next Steps:${NC}"
    echo "  1. Deploy the agent to your production server"
    echo "  2. Update the BASE_URL in this script for network testing"
    echo "  3. Share SUPERVISOR_INTEGRATION.md with your supervisor"
    echo "  4. Provide your deployment URL to the supervisor team"
    echo ""
    echo -e "${YELLOW}API Documentation: $BASE_URL/docs${NC}"
    echo -e "${YELLOW}Dashboard: $BASE_URL/dashboard${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed. Please check the errors above.${NC}"
    echo "Common issues:"
    echo "  - Server not running (run: python main.py)"
    echo "  - Database not connected"
    echo "  - Port 8000 already in use"
fi
echo ""

