#!/bin/bash

echo "=== Updating CloudFront Origin ==="

DISTRIBUTION_ID="E34ZMEPX9776JV"
OLD_API="hqrx8th1fc.execute-api.ap-northeast-1.amazonaws.com"
NEW_API="kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com"

echo "1. Getting current CloudFront config..."
aws cloudfront get-distribution-config --id $DISTRIBUTION_ID > current-config.json

echo "2. Updating Origin from $OLD_API to $NEW_API..."
# ETag を取得
ETAG=$(jq -r '.ETag' current-config.json)

# 設定を更新（古いAPIを新しいAPIに置換）
jq --arg old "$OLD_API" --arg new "$NEW_API" '
  .DistributionConfig.Origins.Items |= map(
    if .DomainName == $old then .DomainName = $new else . end
  ) | 
  del(.ETag)
' current-config.json > updated-config.json

echo "3. Applying CloudFront update..."
aws cloudfront update-distribution \
  --id $DISTRIBUTION_ID \
  --distribution-config file://updated-config.json \
  --if-match $ETAG

echo "4. CloudFront update initiated. Status:"
aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'Distribution.Status' --output text

echo "Updated! allforone-freesite.com/api will now route to $NEW_API"