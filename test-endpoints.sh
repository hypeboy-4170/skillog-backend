#!/bin/bash

echo "=== Testing API Endpoints ==="

echo "1. Testing direct API Gateway:"
curl -X POST https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!","email":"test@example.com"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n2. Testing via CloudFront (after update):"
curl -X POST https://allforone-freesite.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"Test123!","email":"test2@example.com"}' \
  -w "\nStatus: %{http_code}\n"

echo -e "\n3. Testing login:"
curl -X POST https://allforone-freesite.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!"}' \
  -w "\nStatus: %{http_code}\n"