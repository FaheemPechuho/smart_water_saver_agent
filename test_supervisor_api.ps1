# Smart Water Saver Agent - Supervisor API Test Script
# Run this script to test all endpoints before sharing with supervisor

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Smart Water Saver Agent - API Testing Suite         ║" -ForegroundColor Cyan
Write-Host "║  Testing Supervisor-Worker API Contract              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8000"
$testsPassed = 0
$testsFailed = 0

# Function to test endpoint
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [string]$Body = $null
    )
    
    Write-Host "Testing: $Name" -ForegroundColor Yellow
    Write-Host "URL: $Url" -ForegroundColor Gray
    
    try {
        if ($Method -eq "GET") {
            $response = Invoke-WebRequest -Uri $Url -Method $Method -UseBasicParsing
        } else {
            $response = Invoke-WebRequest -Uri $Url -Method $Method -ContentType "application/json" -Body $Body -UseBasicParsing
        }
        
        $json = $response.Content | ConvertFrom-Json
        
        Write-Host "✅ Status Code: $($response.StatusCode)" -ForegroundColor Green
        
        # Verify AgentResponse format
        if ($json.agent_name -and $json.status) {
            Write-Host "✅ Response Format: Valid AgentResponse" -ForegroundColor Green
            Write-Host "   Agent: $($json.agent_name)" -ForegroundColor Gray
            Write-Host "   Status: $($json.status)" -ForegroundColor Gray
            
            if ($json.data -and $json.data.content) {
                $content = $json.data.content
                if ($content.Length -gt 80) {
                    $content = $content.Substring(0, 80) + "..."
                }
                Write-Host "   Response: $content" -ForegroundColor Gray
            }
        } else {
            Write-Host "⚠️  Warning: Response may not follow AgentResponse format" -ForegroundColor Yellow
        }
        
        Write-Host ""
        return $true
        
    } catch {
        Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        return $false
    }
}

Write-Host "Starting tests against: $baseUrl" -ForegroundColor Cyan
Write-Host "Make sure the server is running (python main.py)" -ForegroundColor Yellow
Write-Host ""
Start-Sleep -Seconds 2

# Test 1: Health Check
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST 1: Health Check Endpoint" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
if (Test-Endpoint -Name "Health Check" -Url "$baseUrl/health") {
    $testsPassed++
} else {
    $testsFailed++
}

# Test 2: Root Endpoint
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST 2: Root Endpoint" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
if (Test-Endpoint -Name "Root" -Url "$baseUrl/") {
    $testsPassed++
} else {
    $testsFailed++
}

# Test 3: Chat - Watering Advice
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST 3: Chat - Watering Advice" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
$body = @{
    messages = @(
        @{
            role = "user"
            content = "Should I water my garden today?"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10 -Compress

if (Test-Endpoint -Name "Watering Advice" -Url "$baseUrl/smart-water-saver-agent" -Method "POST" -Body $body) {
    $testsPassed++
} else {
    $testsFailed++
}

# Test 4: Chat - Usage Query
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST 4: Chat - Usage Query" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
$body = @{
    messages = @(
        @{
            role = "user"
            content = "How much water did I use this week?"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10 -Compress

if (Test-Endpoint -Name "Usage Query" -Url "$baseUrl/smart-water-saver-agent" -Method "POST" -Body $body) {
    $testsPassed++
} else {
    $testsFailed++
}

# Test 5: Chat - Water Saving Tip
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST 5: Chat - Water Saving Tip" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
$body = @{
    messages = @(
        @{
            role = "user"
            content = "Give me a water saving tip"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10 -Compress

if (Test-Endpoint -Name "Water Saving Tip" -Url "$baseUrl/smart-water-saver-agent" -Method "POST" -Body $body) {
    $testsPassed++
} else {
    $testsFailed++
}

# Test 6: Chat - Without User ID
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST 6: Chat - Anonymous Request (No User ID)" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
$body = @{
    messages = @(
        @{
            role = "user"
            content = "What are the best times to water plants?"
        }
    )
} | ConvertTo-Json -Depth 10 -Compress

if (Test-Endpoint -Name "Anonymous Chat" -Url "$baseUrl/smart-water-saver-agent" -Method "POST" -Body $body) {
    $testsPassed++
} else {
    $testsFailed++
}

# Test 7: Chat - Multi-turn Conversation
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "TEST 7: Chat - Multi-turn Conversation" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
$body = @{
    messages = @(
        @{
            role = "user"
            content = "What's the weather like?"
        },
        @{
            role = "assistant"
            content = "The weather is partly cloudy."
        },
        @{
            role = "user"
            content = "Should I water based on that?"
        }
    )
    user_id = "test_user_001"
} | ConvertTo-Json -Depth 10 -Compress

if (Test-Endpoint -Name "Multi-turn Conversation" -Url "$baseUrl/smart-water-saver-agent" -Method "POST" -Body $body) {
    $testsPassed++
} else {
    $testsFailed++
}

# Summary
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    TEST SUMMARY                       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "❌ Tests Failed: $testsFailed" -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($testsFailed -eq 0) {
    Write-Host "🎉 ALL TESTS PASSED! Agent is ready for supervisor integration." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Deploy the agent to your production server" -ForegroundColor White
    Write-Host "  2. Update the base URL in this script for network testing" -ForegroundColor White
    Write-Host "  3. Share SUPERVISOR_INTEGRATION.md with your supervisor" -ForegroundColor White
    Write-Host "  4. Provide your deployment URL to the supervisor team" -ForegroundColor White
    Write-Host ""
    Write-Host "API Documentation: $baseUrl/docs" -ForegroundColor Yellow
    Write-Host "Dashboard: $baseUrl/dashboard" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  Some tests failed. Please check the errors above." -ForegroundColor Yellow
    Write-Host "Common issues:" -ForegroundColor White
    Write-Host "  - Server not running (run: python main.py)" -ForegroundColor White
    Write-Host "  - Database not connected" -ForegroundColor White
    Write-Host "  - Port 8000 already in use" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

