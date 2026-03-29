#!/bin/bash

# Automated deployment script for Mock CRM API to IBM Cloud Functions
# Usage: ./deploy-ibm-cloud.sh

set -e  # Exit on error

echo "=========================================="
echo "Mock CRM API - IBM Cloud Deployment"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if IBM Cloud CLI is installed
if ! command -v ibmcloud &> /dev/null; then
    echo -e "${RED}Error: IBM Cloud CLI is not installed${NC}"
    echo ""
    echo "Please install it first:"
    echo "  macOS: curl -fsSL https://clis.cloud.ibm.com/install/osx | sh"
    echo "  Linux: curl -fsSL https://clis.cloud.ibm.com/install/linux | sh"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ IBM Cloud CLI found${NC}"

# Check if Cloud Functions plugin is installed
if ! ibmcloud plugin list | grep -q "cloud-functions"; then
    echo -e "${YELLOW}Installing Cloud Functions plugin...${NC}"
    ibmcloud plugin install cloud-functions -f
fi

echo -e "${GREEN}✓ Cloud Functions plugin ready${NC}"
echo ""

# Check if logged in
if ! ibmcloud target &> /dev/null; then
    echo -e "${YELLOW}You need to login to IBM Cloud${NC}"
    echo "Running: ibmcloud login"
    ibmcloud login
fi

echo -e "${GREEN}✓ Logged in to IBM Cloud${NC}"
echo ""

# Show current target
echo "Current target:"
ibmcloud target
echo ""

# Ask for namespace name
read -p "Enter namespace name (default: mock-crm-api): " NAMESPACE
NAMESPACE=${NAMESPACE:-mock-crm-api}

# Check if namespace exists
if ibmcloud fn namespace list | grep -q "$NAMESPACE"; then
    echo -e "${YELLOW}Namespace '$NAMESPACE' already exists${NC}"
    read -p "Use existing namespace? (y/n): " USE_EXISTING
    if [[ $USE_EXISTING != "y" ]]; then
        echo "Deployment cancelled"
        exit 0
    fi
else
    echo -e "${YELLOW}Creating namespace: $NAMESPACE${NC}"
    ibmcloud fn namespace create "$NAMESPACE"
fi

# Target the namespace
echo "Targeting namespace: $NAMESPACE"
ibmcloud fn namespace target "$NAMESPACE"
echo ""

# Deploy the function
echo -e "${YELLOW}Deploying Mock CRM API function...${NC}"

ACTION_NAME="mock-crm-api"

# Check if action exists
if ibmcloud fn action list | grep -q "$ACTION_NAME"; then
    echo "Action already exists. Updating..."
    ibmcloud fn action update "$ACTION_NAME" \
        crm_api.py \
        --kind python:3.11 \
        --web true \
        --web-secure false
else
    echo "Creating new action..."
    ibmcloud fn action create "$ACTION_NAME" \
        crm_api.py \
        --kind python:3.11 \
        --web true \
        --web-secure false
fi

echo ""
echo -e "${GREEN}✓ Function deployed successfully!${NC}"
echo ""

# Get the function URL
echo "Getting function URL..."
FUNCTION_URL=$(ibmcloud fn action get "$ACTION_NAME" --url | tail -1)

echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Function URL:"
echo -e "${GREEN}$FUNCTION_URL${NC}"
echo ""
echo "To use with JSON responses, append .json:"
echo -e "${GREEN}${FUNCTION_URL}.json${NC}"
echo ""

# Test the function
echo "Testing the function..."
echo ""

echo "1. Testing verify operation (account exists):"
TEST_RESULT=$(curl -s -X POST "${FUNCTION_URL}.json" \
    -H "Content-Type: application/json" \
    -d '{"operation": "verify", "account_number": "ACC12345678"}')

if echo "$TEST_RESULT" | grep -q "account_exists"; then
    echo -e "${GREEN}✓ Test passed!${NC}"
    echo "$TEST_RESULT" | python3 -m json.tool 2>/dev/null || echo "$TEST_RESULT"
else
    echo -e "${RED}✗ Test failed${NC}"
    echo "$TEST_RESULT"
fi

echo ""
echo "2. Testing verify operation (account not found):"
TEST_RESULT=$(curl -s -X POST "${FUNCTION_URL}.json" \
    -H "Content-Type: application/json" \
    -d '{"operation": "verify", "account_number": "ACC99999999"}')

if echo "$TEST_RESULT" | grep -q "account_exists"; then
    echo -e "${GREEN}✓ Test passed!${NC}"
    echo "$TEST_RESULT" | python3 -m json.tool 2>/dev/null || echo "$TEST_RESULT"
else
    echo -e "${RED}✗ Test failed${NC}"
    echo "$TEST_RESULT"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Save this URL for your agent configuration:"
echo "   ${FUNCTION_URL}.json"
echo ""
echo "2. Test with curl:"
echo "   curl -X POST '${FUNCTION_URL}.json' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"operation\": \"verify\", \"account_number\": \"ACC12345678\"}'"
echo ""
echo "3. Update your watsonx Orchestrate agent to use this URL"
echo ""
echo "4. Test account numbers:"
echo "   - ACC12345678 (John Smith)"
echo "   - ACC23456789 (Sarah Johnson)"
echo "   - ACC34567890 (Michael Chen)"
echo ""

# Save URL to file
echo "$FUNCTION_URL.json" > .function-url.txt
echo -e "${GREEN}Function URL saved to: .function-url.txt${NC}"
echo ""

echo "Deployment complete! 🎉"

# Made with Bob
