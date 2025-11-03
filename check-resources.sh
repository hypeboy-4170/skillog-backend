#!/bin/bash

echo "=== AWS Resources Check ==="

echo "1. CloudFront Distributions:"
aws cloudfront list-distributions --query 'DistributionList.Items[*].[Id,DomainName,Status]' --output table

echo -e "\n2. API Gateway APIs:"
aws apigateway get-rest-apis --query 'items[*].[id,name]' --output table

echo -e "\n3. Lambda Functions:"
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime]' --output table

echo -e "\n4. Cognito User Pools:"
aws cognito-idp list-user-pools --max-results 10 --query 'UserPools[*].[Id,Name]' --output table

echo -e "\n5. Check domain allforone-freesite.com:"
nslookup allforone-freesite.com