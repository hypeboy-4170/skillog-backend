#!/bin/bash

echo "=== Emergency API Gateway Deployment ==="

# SAM デプロイで新しい API Gateway を作成
sam build
sam deploy \
  --parameter-overrides \
    UserPoolId=ap-northeast-1_WncgvrLUL \
    ClientId=5ba0ae4io3vsdp5i574tfevo7a \
  --stack-name skillog-api-emergency \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --confirm-changeset

echo "=== Getting new API Gateway URL ==="
aws cloudformation describe-stacks \
  --stack-name skillog-api-emergency \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text