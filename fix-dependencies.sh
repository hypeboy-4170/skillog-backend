#!/bin/bash

echo "=== Installing Linux-compatible dependencies ==="

# 1. 既存のpackageを削除
rm -rf package
mkdir package

# 2. Linux用の依存関係をインストール
pip install \
  --platform linux_x86_64 \
  --target package \
  --implementation cp \
  --python-version 3.9 \
  --only-binary=:all: \
  --upgrade \
  -r requirements.txt

# 3. アプリケーションコードをコピー
cp *.py package/
cp -r services package/

# 4. ZIP作成
cd package
zip -r ../lambda-deployment-linux.zip .
cd ..

# 5. Lambda更新
aws lambda update-function-code \
  --function-name SkilogCdkStack-BackendLambdaSkillogApiLambda78C298-jLViViVYkz5y \
  --zip-file fileb://lambda-deployment-linux.zip

echo "Linux-compatible Lambda deployed!"