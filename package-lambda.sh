#!/bin/bash

echo "=== Packaging Lambda with dependencies ==="

# 1. 依存関係をローカルにインストール
mkdir -p package
pip install -r requirements.txt -t package/

# 2. アプリケーションコードをコピー
cp *.py package/
cp -r services package/

# 3. ZIP ファイル作成
cd package
zip -r ../lambda-deployment.zip .
cd ..

# 4. Lambda 関数を更新
aws lambda update-function-code \
  --function-name SkilogCdkStack-BackendLambdaSkillogApiLambda78C298-jLViViVYkz5y \
  --zip-file fileb://lambda-deployment.zip

echo "Lambda function updated with dependencies!"