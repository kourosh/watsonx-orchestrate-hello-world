# Update Agent with Account Validation

This guide shows how to configure the Customer Complaint Agent to validate account numbers and names against the Mock CRM database.

## What Changed

The agent now:
1. ✅ **Validates account number** - Checks if account exists in CRM
2. ✅ **Validates full name** - Verifies name matches the account
3. ✅ **Allows 3 attempts** - Gives customers multiple tries
4. ✅ **Blocks invalid access** - Only proceeds after successful verification
5. ✅ **Provides clear error messages** - Tells users what went wrong

## Step 1: Get Your Mock CRM URL

After deploying the Mock CRM to IBM Cloud Code Engine, you should have a URL like:
```
https://mock-crm-api.xxxxx.us-south.codeengine.appdomain.cloud
```

If you saved it, check:
```bash
cat /Users/kk76/Public/complaint-agent/mock-crm/.app-url.txt
```

Or retrieve it:
```bash
ibmcloud ce application get --name mock-crm-api --output url
```

## Step 2: Update the OpenAPI Spec with Your URL

Edit the file: `tools/account-verification-openapi.yaml`

Replace line 8:
```yaml
servers:
  - url: https://YOUR_CODE_ENGINE_URL  # Replace with your actual URL
```

With your actual URL:
```yaml
servers:
  - url: https://mock-crm-api.xxxxx.us-south.codeengine.appdomain.cloud
```

## Step 3: Import the Tool into Orchestrate

### Option A: Using Orchestrate CLI

```bash
cd /Users/kk76/Public/complaint-agent

# Import the OpenAPI tool
orchestrate tools import \
  --kind openapi \
  --file tools/account-verification-openapi.yaml
```

### Option B: Using Orchestrate Web UI

1. Go to your Orchestrate workspace
2. Navigate to **Tools** → **Import**
3. Select **OpenAPI**
4. Upload `tools/account-verification-openapi.yaml`
5. Click **Import**

## Step 4: Update the Agent to Use the Tool

### Option A: Using Orchestrate CLI

```bash
# Re-import the updated agent
orchestrate agents import \
  --file agents/customer-complaint-agent.yaml
```

### Option B: Using Orchestrate Web UI

1. Go to **Agents** → **CustomerComplaintAgent**
2. Click **Edit**
3. Go to **Tools** section
4. Click **Add Tool**
5. Select **Mock CRM Account Verification API**
6. Enable these operations:
   - `getAccountDetails` (primary - for full verification)
   - `verifyAccount` (optional - for quick checks)
7. Click **Save**

## Step 5: Test the Validation

### Test Case 1: Valid Account and Name ✅

```
Agent: Hello! Thank you for contacting us today. I'm here to help you with any concerns. 
       Before we begin, I'll need to verify your account information.
       
       May I have your account number?

You: ACC12345678

Agent: Thank you. Could you please provide your full name?

You: John Smith

Agent: Thank you, John Smith. I've verified your account ACC12345678. 
       Now, please tell me about your concern.
```

### Test Case 2: Valid Account, Wrong Name ❌

```
Agent: May I have your account number?

You: ACC12345678

Agent: Thank you. Could you please provide your full name?

You: Jane Doe

Agent: I'm sorry, the name you provided doesn't match our records for this account. 
       Please verify your information. You have 2 more attempts.
```

### Test Case 3: Invalid Account Number ❌

```
Agent: May I have your account number?

You: ACC99999999

Agent: I'm sorry, I couldn't find an account with that number. 
       Please verify and try again. You have 2 more attempts.
```

## Valid Test Accounts

Use these for testing:

| Account Number | Full Name | Email | Type |
|---------------|-----------|-------|------|
| ACC12345678 | John Smith | john.smith@email.com | Premium |
| ACC23456789 | Sarah Johnson | sarah.johnson@email.com | Standard |
| ACC34567890 | Michael Chen | michael.chen@email.com | Premium |
| ACC45678901 | Emily Davis | emily.davis@email.com | Standard |
| ACC56789012 | Robert Martinez | robert.martinez@email.com | Premium |

## How the Validation Works

1. **User provides account number**
   - Agent calls: `GET /api/v1/accounts/{account_number}`
   - Checks if account exists

2. **User provides name**
   - Agent compares provided name with `full_name` from CRM response
   - Must match exactly (case-insensitive comparison recommended)

3. **Validation passes**
   - Agent proceeds to collect complaint details
   - User can now report their issue

4. **Validation fails**
   - Agent provides specific error message
   - Allows retry (up to 3 attempts total)
   - After 3 failures, escalates to verification team

## Troubleshooting

### Tool not appearing in agent
**Solution:** Make sure you've imported the OpenAPI spec and linked it to the agent

### "Cannot connect to API"
**Solution:** 
1. Verify Mock CRM is deployed: `curl YOUR_URL/health`
2. Check the URL in the OpenAPI spec is correct
3. Ensure Code Engine app is running

### Agent not validating
**Solution:**
1. Check agent instructions were updated
2. Verify tool is enabled in agent configuration
3. Test the API endpoint directly with curl

### Name validation too strict
**Solution:** The agent should do case-insensitive comparison. If issues persist, update the instructions to be more flexible with name matching (e.g., "John Smith" = "john smith")

## Advanced Configuration

### Custom Validation Rules

You can modify the agent instructions to add:
- Middle name handling
- Nickname support
- Partial name matching
- Additional security questions

### Logging and Monitoring

To track validation attempts:
1. Enable logging in Code Engine
2. Monitor failed validation attempts
3. Set up alerts for suspicious activity

## Security Notes

⚠️ **Important:**
- This is a demo setup with basic validation
- For production, add:
  - Rate limiting on validation attempts
  - Account lockout after failed attempts
  - Audit logging of all validation attempts
  - Multi-factor authentication
  - Encrypted communication

## Next Steps

After validation is working:
1. ✅ Test with all sample accounts
2. ✅ Verify error messages are clear
3. ✅ Test the 3-attempt limit
4. ✅ Proceed to complaint collection after validation
5. ✅ Demo the complete flow

---

**Quick Start:**
```bash
# 1. Get your CRM URL
cat /Users/kk76/Public/complaint-agent/mock-crm/.app-url.txt

# 2. Update OpenAPI spec with URL
# Edit: tools/account-verification-openapi.yaml

# 3. Import tool
orchestrate tools import --kind openapi --file tools/account-verification-openapi.yaml

# 4. Re-import agent
orchestrate agents import --file agents/customer-complaint-agent.yaml

# 5. Test!