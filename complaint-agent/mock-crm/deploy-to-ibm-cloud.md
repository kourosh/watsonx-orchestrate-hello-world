# Deploy Mock CRM API to IBM Cloud Functions

This guide will help you deploy the Mock CRM API to IBM Cloud Functions.

## Prerequisites

1. IBM Cloud account (you have this ✓)
2. IBM Cloud CLI installed
3. IBM Cloud Functions plugin installed

## Step 1: Install IBM Cloud CLI

### macOS
```bash
curl -fsSL https://clis.cloud.ibm.com/install/osx | sh
```

### Linux
```bash
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
```

### Windows
Download from: https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases

### Verify Installation
```bash
ibmcloud --version
```

## Step 2: Install Cloud Functions Plugin

```bash
ibmcloud plugin install cloud-functions
```

## Step 3: Login to IBM Cloud

```bash
ibmcloud login
```

If you have SSO:
```bash
ibmcloud login --sso
```

## Step 4: Target Your Region and Resource Group

```bash
# List available regions
ibmcloud regions

# Target a region (e.g., us-south)
ibmcloud target -r us-south

# List resource groups
ibmcloud resource groups

# Target a resource group
ibmcloud target -g Default
```

## Step 5: Create a Namespace for Cloud Functions

```bash
# Create namespace
ibmcloud fn namespace create mock-crm-api

# Target the namespace
ibmcloud fn namespace target mock-crm-api
```

## Step 6: Deploy the Function

Navigate to the mock-crm directory:
```bash
cd /Users/kk76/Public/complaint-agent/mock-crm
```

Deploy the function:
```bash
ibmcloud fn action create mock-crm-verify \
  crm_api.py \
  --kind python:3.11 \
  --web true \
  --web-secure false
```

## Step 7: Get the Function URL

```bash
ibmcloud fn action get mock-crm-verify --url
```

You'll get a URL like:
```
https://us-south.functions.cloud.ibm.com/api/v1/web/YOUR_NAMESPACE/default/mock-crm-verify
```

## Step 8: Test the Function

### Verify Account (exists)
```bash
curl -X POST "https://YOUR_FUNCTION_URL.json" \
  -H "Content-Type: application/json" \
  -d '{"operation": "verify", "account_number": "ACC12345678"}'
```

### Get Account Details
```bash
curl -X POST "https://YOUR_FUNCTION_URL.json" \
  -H "Content-Type: application/json" \
  -d '{"operation": "get_details", "account_number": "ACC12345678"}'
```

### List All Customers
```bash
curl -X POST "https://YOUR_FUNCTION_URL.json" \
  -H "Content-Type: application/json" \
  -d '{"operation": "list_all"}'
```

## Step 9: Update Your Agent Configuration

Once deployed, update your agent's tool configuration with the IBM Cloud Functions URL.

Edit `agents/customer-complaint-agent.yaml` or configure in Orchestrate UI:
```yaml
integrations:
  - name: account_lookup
    type: api
    url: "https://YOUR_FUNCTION_URL.json"
```

## Alternative: Deploy as Code Engine Application

If you prefer a REST API instead of Functions:

### 1. Create Code Engine Project
```bash
ibmcloud ce project create --name mock-crm-api
ibmcloud ce project select --name mock-crm-api
```

### 2. Deploy from Source
```bash
cd /Users/kk76/Public/complaint-agent/mock-crm

ibmcloud ce application create \
  --name mock-crm-api \
  --build-source . \
  --strategy dockerfile \
  --port 8080 \
  --min-scale 1 \
  --max-scale 2 \
  --cpu 0.25 \
  --memory 0.5G
```

### 3. Get the URL
```bash
ibmcloud ce application get --name mock-crm-api --output url
```

### 4. Test
```bash
curl https://YOUR_CODE_ENGINE_URL/api/v1/accounts/ACC12345678/verify
```

## Automated Deployment Script

I've created a script to automate this. Run:

```bash
cd /Users/kk76/Public/complaint-agent/mock-crm
chmod +x deploy-ibm-cloud.sh
./deploy-ibm-cloud.sh
```

## Troubleshooting

### "Command not found: ibmcloud"
Install the IBM Cloud CLI (see Step 1)

### "You are not logged in"
Run: `ibmcloud login`

### "No namespace targeted"
Run: `ibmcloud fn namespace target mock-crm-api`

### "Action already exists"
Update instead:
```bash
ibmcloud fn action update mock-crm-verify crm_api.py --kind python:3.11 --web true
```

### "Function returns error"
Check logs:
```bash
ibmcloud fn activation poll
```

## Cost Considerations

**IBM Cloud Functions:**
- Free tier: 400,000 GB-seconds per month
- This demo will use minimal resources
- Estimated cost: $0/month (within free tier)

**Code Engine:**
- Free tier: 100,000 vCPU-seconds per month
- This demo will use minimal resources
- Estimated cost: $0-5/month

## Security Notes

⚠️ **Important for Production:**
- Enable `--web-secure true` for authentication
- Add API key validation
- Use HTTPS only
- Implement rate limiting
- Add logging and monitoring

For this demo, we're using `--web-secure false` for simplicity.

## Next Steps

1. Install IBM Cloud CLI
2. Login to your account
3. Run the deployment script
4. Get the function URL
5. Update your agent configuration
6. Test with your Orchestrate agent!

## Support

If you encounter issues:
- IBM Cloud Docs: https://cloud.ibm.com/docs/openwhisk
- IBM Cloud Support: https://cloud.ibm.com/unifiedsupport/supportcenter