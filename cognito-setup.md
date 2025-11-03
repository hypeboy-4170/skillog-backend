# Cognito セットアップ手順

## 1. User Pool 作成
```bash
aws cognito-idp create-user-pool --pool-name skillog-users
```

## 2. User Pool Client 作成
```bash
aws cognito-idp create-user-pool-client \
  --user-pool-id YOUR_USER_POOL_ID \
  --client-name skillog-client \
  --explicit-auth-flows ADMIN_NO_SRP_AUTH
```

## 3. テストユーザー作成
```bash
aws cognito-idp admin-create-user \
  --user-pool-id YOUR_USER_POOL_ID \
  --username testuser \
  --temporary-password TempPass123! \
  --message-action SUPPRESS
```

## 4. パスワード設定
```bash
aws cognito-idp admin-set-user-password \
  --user-pool-id YOUR_USER_POOL_ID \
  --username testuser \
  --password Password123! \
  --permanent
```