# CloudFront 403エラー修正方法

## 修正が必要な場所: **AWS Console または CLI**

CloudFrontの設定はSAM templateに含まれていないため、以下の方法で修正する必要があります。

## 修正方法

### 1. AWS Console での修正 (推奨)

1. **CloudFront Console** にアクセス
2. **Distribution ID: E34ZMEPX9776JV** を選択
3. **Behaviors** タブを選択
4. **/api/*** パターンを編集
5. 以下を変更:
   - **Cache Policy**: `CachingDisabled`
   - **Origin Request Policy**: `AllViewer`
   - **Response Headers Policy**: `CORS-with-preflight-and-SecurityHeadersPolicy`

### 2. CLI での修正

```bash
# 現在の設定を取得
aws cloudfront get-distribution-config --id E34ZMEPX9776JV > current-config.json

# ETagを取得
ETAG=$(jq -r '.ETag' current-config.json)

# 設定を更新 (Cache PolicyとOrigin Request Policyを変更)
jq '.DistributionConfig.CacheBehaviors.Items[] |= 
  if .PathPattern == "/api/*" then 
    .CachePolicyId = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad" |
    .OriginRequestPolicyId = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"
  else . end | del(.ETag)' current-config.json > updated-config.json

# 更新を適用
aws cloudfront update-distribution \
  --id E34ZMEPX9776JV \
  --distribution-config file://updated-config.json \
  --if-match $ETAG
```

### 3. SAM Template への追加 (将来的な改善)

```yaml
# template.yaml に追加
CloudFrontDistribution:
  Type: AWS::CloudFront::Distribution
  Properties:
    DistributionConfig:
      Origins:
        - Id: api-gateway-origin
          DomainName: !Sub "${SkillogApi}.execute-api.${AWS::Region}.amazonaws.com"
          OriginPath: /prod
          CustomOriginConfig:
            HTTPPort: 443
            OriginProtocolPolicy: https-only
      DefaultCacheBehavior:
        TargetOriginId: s3-origin
        ViewerProtocolPolicy: redirect-to-https
      CacheBehaviors:
        - PathPattern: "/api/*"
          TargetOriginId: api-gateway-origin
          ViewerProtocolPolicy: redirect-to-https
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad  # CachingDisabled
          OriginRequestPolicyId: 88a5eaf4-2fd4-4709-b370-b4c650ea3fcf  # AllViewer
          AllowedMethods:
            - GET
            - HEAD
            - OPTIONS
            - PUT
            - POST
            - PATCH
            - DELETE
```

## 修正後の確認

```bash
python test_correct_cloudfront.py
```

## 結論

**AWS Console** での手動修正が最も確実で迅速な解決方法です。