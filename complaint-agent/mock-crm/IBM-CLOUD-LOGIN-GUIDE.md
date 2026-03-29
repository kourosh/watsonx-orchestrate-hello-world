# IBM Cloud Login Guide - Federated User

Since you're using a federated user ID (SSO), you need to use either SSO login or an API key.

## Option 1: SSO Login (Quickest)

### Step 1: Start SSO Login
```bash
ibmcloud login --sso
```

### Step 2: Get One-Time Passcode
The CLI will display a URL like:
```
Get a one-time code from https://identity-1.us-south.iam.cloud.ibm.com/identity/passcode to proceed.
Open the URL in the default browser? [Y/n] >
```

Press `Y` or just hit Enter.

### Step 3: Copy the Passcode
- Your browser will open
- Login with your IBM Cloud credentials
- Copy the one-time passcode displayed

### Step 4: Paste the Passcode
Return to your terminal and paste the passcode when prompted:
```
One-time code > [paste your code here]
```

### Step 5: Select Account
If you have multiple accounts, select the one you want to use.

**Done!** You're now logged in.

---

## Option 2: API Key Login (Recommended for Automation)

### Step 1: Create an API Key

#### Via Web Console:
1. Go to https://cloud.ibm.com
2. Click on **Manage** → **Access (IAM)** in the top menu
3. Click **API keys** in the left sidebar
4. Click **Create +** button
5. Enter a name: `mock-crm-deployment`
6. Enter a description: `API key for deploying Mock CRM API`
7. Click **Create**
8. **IMPORTANT:** Copy the API key immediately (you won't see it again!)
9. Click **Download** to save it as a file (recommended)

#### Via CLI (Alternative):
```bash
# First login with SSO
ibmcloud login --sso

# Create API key
ibmcloud iam api-key-create mock-crm-deployment \
  -d "API key for deploying Mock CRM API" \
  --file ~/mock-crm-api-key.json
```

### Step 2: Save Your API Key Securely

**Option A: Save to a file**
```bash
# Create a secure file
echo "YOUR_API_KEY_HERE" > ~/.ibmcloud-api-key
chmod 600 ~/.ibmcloud-api-key
```

**Option B: Use environment variable**
```bash
# Add to your ~/.zshrc or ~/.bashrc
export IBMCLOUD_API_KEY="YOUR_API_KEY_HERE"
source ~/.zshrc  # or ~/.bashrc
```

### Step 3: Login with API Key

**From file:**
```bash
ibmcloud login --apikey @~/.ibmcloud-api-key
```

**From environment variable:**
```bash
ibmcloud login --apikey $IBMCLOUD_API_KEY
```

**Direct (not recommended - visible in history):**
```bash
ibmcloud login --apikey YOUR_API_KEY_HERE
```

### Step 4: Verify Login
```bash
ibmcloud target
```

You should see your account information.

---

## Quick Reference

### Login Commands

```bash
# SSO Login
ibmcloud login --sso

# API Key from file
ibmcloud login --apikey @~/.ibmcloud-api-key

# API Key from environment
ibmcloud login --apikey $IBMCLOUD_API_KEY

# Specify region during login
ibmcloud login --sso -r us-south

# Check current login status
ibmcloud target
```

### After Login - Deploy Mock CRM

```bash
cd /Users/kk76/Public/complaint-agent/mock-crm
./deploy-code-engine.sh
```

---

## Troubleshooting

### "You are using a federated user ID"
**Solution:** Use `--sso` flag or API key

### "API key is invalid"
**Solution:** 
1. Verify the API key is correct
2. Check if the API key has been deleted
3. Create a new API key

### "No region targeted"
**Solution:**
```bash
ibmcloud target -r us-south
```

### "No resource group targeted"
**Solution:**
```bash
ibmcloud target -g Default
```

---

## Recommended Setup for This Demo

### One-Time Setup:

1. **Create API Key** (via web console - easier)
   - Go to https://cloud.ibm.com
   - Manage → Access (IAM) → API keys
   - Create → Copy → Save

2. **Save API Key Securely**
   ```bash
   echo "YOUR_API_KEY" > ~/.ibmcloud-api-key
   chmod 600 ~/.ibmcloud-api-key
   ```

3. **Login**
   ```bash
   ibmcloud login --apikey @~/.ibmcloud-api-key -r us-south
   ```

4. **Deploy**
   ```bash
   cd /Users/kk76/Public/complaint-agent/mock-crm
   ./deploy-code-engine.sh
   ```

### For Future Logins:

```bash
# Just run this one command
ibmcloud login --apikey @~/.ibmcloud-api-key -r us-south
```

---

## Security Best Practices

✅ **DO:**
- Store API keys in secure files with restricted permissions (chmod 600)
- Use environment variables for automation
- Create separate API keys for different purposes
- Delete API keys you no longer need
- Rotate API keys periodically

❌ **DON'T:**
- Commit API keys to git
- Share API keys in chat/email
- Use the same API key everywhere
- Store API keys in plain text in public places

---

## Next Steps

After successful login:

1. ✅ Verify login: `ibmcloud target`
2. ✅ Install Code Engine plugin: `ibmcloud plugin install code-engine`
3. ✅ Deploy: `cd /Users/kk76/Public/complaint-agent/mock-crm && ./deploy-code-engine.sh`

---

## Need Help?

- IBM Cloud Docs: https://cloud.ibm.com/docs/cli
- API Key Management: https://cloud.ibm.com/docs/account?topic=account-userapikey
- Code Engine Docs: https://cloud.ibm.com/docs/codeengine