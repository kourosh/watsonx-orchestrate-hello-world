#!/bin/bash

# Test script for Mock CRM API
# Usage: ./test_api.sh [API_URL]

API_URL="${1:-http://localhost:8080}"

echo "=========================================="
echo "Testing Mock CRM API"
echo "API URL: $API_URL"
echo "=========================================="
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Warning: jq is not installed. Output will not be formatted."
    echo "Install with: brew install jq (macOS) or apt-get install jq (Linux)"
    JQ_CMD="cat"
else
    JQ_CMD="jq"
fi

echo "1. Health Check:"
echo "GET $API_URL/health"
curl -s $API_URL/health | $JQ_CMD
echo ""
echo ""

echo "2. Verify Account (exists):"
echo "GET $API_URL/api/v1/accounts/ACC12345678/verify"
curl -s $API_URL/api/v1/accounts/ACC12345678/verify | $JQ_CMD
echo ""
echo ""

echo "3. Verify Account (not found):"
echo "GET $API_URL/api/v1/accounts/ACC99999999/verify"
curl -s $API_URL/api/v1/accounts/ACC99999999/verify | $JQ_CMD
echo ""
echo ""

echo "4. Get Account Details:"
echo "GET $API_URL/api/v1/accounts/ACC12345678"
curl -s $API_URL/api/v1/accounts/ACC12345678 | $JQ_CMD
echo ""
echo ""

echo "5. List All Customers:"
echo "GET $API_URL/api/v1/customers"
curl -s $API_URL/api/v1/customers | $JQ_CMD '.count'
echo " customers found"
echo ""
echo ""

echo "6. Search Customers (query: john):"
echo "GET $API_URL/api/v1/customers/search?q=john"
curl -s "$API_URL/api/v1/customers/search?q=john" | $JQ_CMD
echo ""
echo ""

echo "=========================================="
echo "All tests completed!"
echo "=========================================="

# Made with Bob
