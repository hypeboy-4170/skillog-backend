# Final API Test - Direct API Gateway

$apiUrl = "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod"

Write-Host "=== Final API Test ===" -ForegroundColor Cyan

# Test 1: Register new user
Write-Host "`n1. Testing Register..." -ForegroundColor Yellow
$registerBody = @{
    username = "finaltest"
    password = "Test123!"
    email = "finaltest@example.com"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-RestMethod -Uri "$apiUrl/register" -Method POST -Body $registerBody -ContentType "application/json"
    Write-Host "✅ Register Success: $($registerResponse.message)" -ForegroundColor Green
    $registerSuccess = $true
} catch {
    Write-Host "❌ Register Error: $($_.Exception.Message)" -ForegroundColor Red
    $registerSuccess = $false
}

# Test 2: Login with registered user
if ($registerSuccess) {
    Write-Host "`n2. Testing Login..." -ForegroundColor Yellow
    $loginBody = @{
        username = "finaltest"
        password = "Test123!"
    } | ConvertTo-Json

    try {
        $loginResponse = Invoke-RestMethod -Uri "$apiUrl/login" -Method POST -Body $loginBody -ContentType "application/json"
        Write-Host "✅ Login Success: Token received" -ForegroundColor Green
        $token = $loginResponse.access_token
        Write-Host "   Token preview: $($token.Substring(0,30))..." -ForegroundColor Gray
        $loginSuccess = $true
    } catch {
        Write-Host "❌ Login Error: $($_.Exception.Message)" -ForegroundColor Red
        $loginSuccess = $false
    }
}

# Test 3: Send Email with token
if ($loginSuccess -and $token) {
    Write-Host "`n3. Testing Send Email..." -ForegroundColor Yellow
    $emailBody = @{
        to = "recipient@example.com"
        subject = "Test Email from API"
        body = "This is a test email sent via API Gateway and Lambda"
    } | ConvertTo-Json

    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }

    try {
        $emailResponse = Invoke-RestMethod -Uri "$apiUrl/sendmail" -Method POST -Body $emailBody -Headers $headers
        Write-Host "✅ Email Success: $($emailResponse.message)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Email Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== Test Summary ===" -ForegroundColor Cyan
Write-Host "API URL: $apiUrl" -ForegroundColor White
Write-Host "Register: $(if($registerSuccess){'✅ PASS'}else{'❌ FAIL'})" -ForegroundColor $(if($registerSuccess){'Green'}else{'Red'})
Write-Host "Login: $(if($loginSuccess){'✅ PASS'}else{'❌ FAIL'})" -ForegroundColor $(if($loginSuccess){'Green'}else{'Red'})
Write-Host "SendMail: $(if($token){'✅ TESTED'}else{'❌ SKIPPED'})" -ForegroundColor $(if($token){'Green'}else{'Yellow'})