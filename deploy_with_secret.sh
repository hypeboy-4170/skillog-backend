#!/bin/bash

echo "=== Cognito CLIENT_SECRET付きデプロイ ==="

# CLIENT_SECRETを取得（実際の値は手動で設定）
read -s -p "Cognito Client Secret を入力してください: " CLIENT_SECRET
echo

# SAMデプロイ
sam deploy \
  --template-file template.yaml \
  --stack-name skillog-backend \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    UserPoolId=ap-northeast-1_WncgvrLUL \
    ClientId=5ba0ae4io3vsdp5i574tfevo7a \
    ClientSecret=$CLIENT_SECRET

echo "デプロイ完了"