# PowerShell用デプロイスクリプト

Write-Host "=== Cognito CLIENT_SECRET付きデプロイ ===" -ForegroundColor Green

# CLIENT_SECRETを設定
$CLIENT_SECRET = "1cf7q4beajh4jjcqm04os3hkqbe7mbp6gdv46qrgd3esegrkj1hi"

# SAMデプロイ
sam deploy `
  --template-file template.yaml `
  --stack-name skillog-backend `
  --capabilities CAPABILITY_IAM `
  --parameter-overrides `
    UserPoolId=ap-northeast-1_WncgvrLUL `
    ClientId=5ba0ae4io3vsdp5i574tfevo7a `
    ClientSecret=$CLIENT_SECRET

Write-Host "デプロイ完了" -ForegroundColor Green