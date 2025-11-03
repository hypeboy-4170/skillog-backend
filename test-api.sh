#!/bin/bash

echo "=== API Access Test ==="

API_URL="https://kuu6xkur5i.execute-api.ap-northeast-1.amazonaws.com/prod"
CLOUDFRONT_URL="https://allforone-freesite.com/api"

echo "1. Testing direct API Gateway - Register:"
curl -X POST $API_URL/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser1","password":"Test123!","email":"test1@example.com"}' \
  -w "\nHTTP Status: %{http_code}\n\n"

echo "2. Testing direct API Gateway - Login:"
curl -X POST $API_URL/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser1","password":"Test123!"}' \
  -w "\nHTTP Status: %{http_code}\n\n"

echo "3. Testing CloudFront - Register:"
curl -X POST $CLOUDFRONT_URL/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"Test123!","email":"test2@example.com"}' \
  -w "\nHTTP Status: %{http_code}\n\n"

echo "4. Testing CloudFront - Login:"
curl -X POST $CLOUDFRONT_URL/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"Test123!"}' \
  -w "\nHTTP Status: %{http_code}\n\n"