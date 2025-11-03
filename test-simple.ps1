# Simple API Test

$apiUrl = "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod"

Write-Host "Testing Login with existing user..."

$loginBody = @{
    username = "testuser1"
    password = "Test123!"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$apiUrl/login" -Method POST -Body $loginBody -ContentType "application/json"
    Write-Host "Login Success!" -ForegroundColor Green
    Write-Host "Token: $($response.access_token.Substring(0,20))..." -ForegroundColor Yellow
} catch {
    Write-Host "Login Error: $($_.Exception.Message)" -ForegroundColor Red
}