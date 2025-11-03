#!/bin/bash

echo "=== Redeploying with correct stage ==="

# 既存スタックを削除して再作成
aws cloudformation delete-stack --stack-name skillog-backend --region ap-northeast-1

echo "Waiting for stack deletion..."
aws cloudformation wait stack-delete-complete --stack-name skillog-backend --region ap-northeast-1

echo "Redeploying with correct configuration..."
sam build
sam deploy \
  --parameter-overrides \
    UserPoolId=ap-northeast-1_WncgvrLUL \
    ClientId=5ba0ae4io3vsdp5i574tfevo7a \
  --stack-name skillog-backend \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --confirm-changeset

echo "Getting new API URL..."
aws cloudformation describe-stacks \
  --stack-name skillog-backend \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text