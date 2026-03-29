#!/bin/bash

# Automated deployment script for Mock CRM API to IBM Cloud Code Engine
# Usage: ./deploy-code-engine.sh

set -e  # Exit on error

echo "=========================================="
echo "Mock CRM API - IBM Cloud Code Engine Deployment"
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

# Check if Code Engine plugin is installed
if ! ibmcloud plugin list | grep -q "code-engine"; then
    echo -e "${YELLOW}Installing Code Engine plugin...${NC}"
    ibmcloud plugin install code-engine -f
fi

echo -e "${GREEN}✓ Code Engine plugin ready${NC}"
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

# Ask for project name
read -p "Enter Code Engine project name (default: mock-crm-api): " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-mock-crm-api}

# Check if project exists
if ibmcloud ce project list 2>/dev/null | grep -q "$PROJECT_NAME"; then
    echo -e "${YELLOW}Project '$PROJECT_NAME' already exists${NC}"
    read -p "Use existing project? (y/n): " USE_EXISTING
    if [[ $USE_EXISTING != "y" ]]; then
        echo "Deployment cancelled"
        exit 0
    fi
    ibmcloud ce project select --name "$PROJECT_NAME"
else
    echo -e "${YELLOW}Creating project: $PROJECT_NAME${NC}"
    ibmcloud ce project create --name "$PROJECT_NAME"
    ibmcloud ce project select --name "$PROJECT_NAME"
fi

echo ""

# Deploy the application
echo -e "${YELLOW}Deploying Mock CRM API application...${NC}"

APP_NAME="mock-crm-api"

# Check if app exists
if ibmcloud ce app list 2>/dev/null | grep -q "$APP_NAME"; then
    echo "Application already exists. Updating..."
    ibmcloud ce app update --name "$APP_NAME" \
        --build-source . \
        --port 8080 \
        --min-scale 0 \
        --max-scale 1 \
        --cpu 0.25 \
        --memory 0.5G \
        --wait
else
    echo "Creating new application..."
    ibmcloud ce app create --name "$APP_NAME" \
        --build-source . \
        --port 8080 \
        --min-scale 0 \
        --max-scale 1 \
        --cpu 0.25 \
        --memory 0.5G \
        --wait
fi

echo ""
echo -e "${GREEN}✓ Application deployed successfully!${NC}"
echo ""

# Get the application URL
echo "Getting application URL..."
APP_URL=$(ibmcloud ce app get --name "$APP_NAME" --output url 2>/dev/null | grep -v "Getting" | grep -v "OK")

echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Application URL:"
echo -e "${GREEN}$APP_URL${NC}"
echo ""

# Wait for app to be ready
echo "Waiting for application to be ready..."
sleep 10

# Test the application
echo "Testing the application..."
echo ""

echo "1. Testing health endpoint:"
HEALTH_RESULT=$(curl -s "${APP_URL}/health" || echo "Failed to connect")

if echo "$HEALTH_RESULT" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed!${NC}"
    echo "$HEALTH_RESULT" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESULT"
else
    echo -e "${YELLOW}⚠ Health check pending (app may still be starting)${NC}"
    echo "$HEALTH_RESULT"
fi

echo ""
echo "2. Testing verify account (exists):"
VERIFY_RESULT=$(curl -s "${APP_URL}/api/v1/accounts/ACC12345678/verify" || echo "Failed to connect")

if echo "$VERIFY_RESULT" | grep -q "account_exists"; then
    echo -e "${GREEN}✓ Verify test passed!${NC}"
    echo "$VERIFY_RESULT" | python3 -m json.tool 2>/dev/null || echo "$VERIFY_RESULT"
else
    echo -e "${YELLOW}⚠ Verify test pending (app may still be starting)${NC}"
    echo "$VERIFY_RESULT"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Save this URL for your agent configuration:"
echo "   ${APP_URL}"
echo ""
echo "2. API Endpoints:"
echo "   Verify: ${APP_URL}/api/v1/accounts/{account_number}/verify"
echo "   Details: ${APP_URL}/api/v1/accounts/{account_number}"
echo "   List: ${APP_URL}/api/v1/customers"
echo ""
echo "3. Test with curl:"
echo "   curl ${APP_URL}/api/v1/accounts/ACC12345678/verify"
echo ""
echo "4. Update your watsonx Orchestrate agent to use this URL"
echo ""
echo "5. Test account numbers:"
echo "   - ACC12345678 (John Smith)"
echo "   - ACC23456789 (Sarah Johnson)"
echo "   - ACC34567890 (Michael Chen)"
echo ""

# Save URL to file
echo "$APP_URL" > .app-url.txt
echo -e "${GREEN}Application URL saved to: .app-url.txt${NC}"
echo ""

echo "Deployment complete! 🎉"
echo ""
echo "Note: If tests failed, the app may still be starting."
echo "Wait 30 seconds and try: curl ${APP_URL}/health"

# Made with Bob
