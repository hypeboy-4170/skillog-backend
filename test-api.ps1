# PowerShell API Test Script

$apiUrl = "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod"

Write-Host "=== API Test ==="

# Test 1: Register
Write-Host "1. Testing Register..."
$registerBody = @{
    username = "newuser"
    password = "Test123!"
    email = "new@example.com"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$apiUrl/register" -Method POST -Body $registerBody -ContentType "application/json"
    Write-Host "Register Success: $($response.message)" -ForegroundColor Green
} catch {
    Write-Host "Register Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Login
Write-Host "`n2. Testing Login..."
$loginBody = @{
    username = "newuser"
    password = "Test123!"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$apiUrl/login" -Method POST -Body $loginBody -ContentType "application/json"
    Write-Host "Login Success: Token received" -ForegroundColor Green
    $token = $response.access_token
} catch {
    Write-Host "Login Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Send Email (if token exists)
if ($token) {
    Write-Host "`n3. Testing Send Email..."
    $emailBody = @{
        to = "test@example.com"
        subject = "Test Email"
        body = "This is a test email"
    } | ConvertTo-Json

    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }

    try {
        $response = Invoke-RestMethod -Uri "$apiUrl/sendmail" -Method POST -Body $emailBody -Headers $headers
        Write-Host "Email Success: $($response.message)" -ForegroundColor Green
    } catch {
        Write-Host "Email Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== Test Complete ==="