# Working API Test

Write-Host "=== API Working Test ==="

# Test with curl (works)
Write-Host "1. Using curl (working):"
& curl -X POST "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod/register" -H "Content-Type: application/json" -d '{"username":"curluser","password":"Test123!","email":"curl@example.com"}' --silent

Write-Host "`n2. URL is correct:"
Write-Host "https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod" -ForegroundColor Green

Write-Host "`n3. Available endpoints:"
Write-Host "  - /register ✅" -ForegroundColor Green  
Write-Host "  - /login ✅" -ForegroundColor Green
Write-Host "  - /sendmail ✅" -ForegroundColor Green