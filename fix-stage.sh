#!/bin/bash

echo "=== Fixing API Gateway Stage ==="

# 現在のAPI Gateway IDを取得
API_ID="kuu6xkur5i"

echo "1. Creating prod stage..."
aws apigateway create-stage \
  --rest-api-id $API_ID \
  --stage-name prod \
  --deployment-id $(aws apigateway get-deployments --rest-api-id $API_ID --query 'items[0].id' --output text) \
  --region ap-northeast-1

echo "2. Testing prod endpoint..."
echo "New endpoint: https://$API_ID.execute-api.ap-northeast-1.amazonaws.com/prod/"

echo "3. Test register endpoint:"
curl -X POST https://$API_ID.execute-api.ap-northeast-1.amazonaws.com/prod/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!","email":"test@example.com"}'