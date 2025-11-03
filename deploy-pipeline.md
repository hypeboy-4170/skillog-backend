# CodePipeline デプロイ手順

## 1. リポジトリにプッシュ
```bash
git add .
git commit -m "Deploy FastAPI Lambda function"
git push origin main
```

## 2. CodePipeline 確認
- AWS Console → CodePipeline
- パイプライン名: `SkilogCdkStack-BackendPipeline`
- ビルド状況を監視

## 3. デプロイ後テスト
```bash
# Register テスト
curl -X POST https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!","email":"test@example.com"}'

# Login テスト  
curl -X POST https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!"}'
```

## 4. 現在の状況
- ✅ Lambda関数: 正常動作
- ✅ API Gateway: エンドポイント作成済み
- ✅ Cognito: ユーザー作成可能
- 🔄 CodePipeline: デプロイ準備完了