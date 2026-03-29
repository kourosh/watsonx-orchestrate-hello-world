# Quick Start Guide - Customer Complaint Agent

Get the Customer Complaint Agent up and running in minutes for testing and development.

## 🚀 Quick Setup (5 minutes)

### 1. Prerequisites Check

```bash
# Verify you have access to:
# ✓ IBM watsonx Orchestrate account
# ✓ watsonx.ai with Granite model
# ✓ API credentials ready
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials (minimum required):
WATSONX_API_KEY=your_key_here
WATSONX_PROJECT_ID=your_project_id
ACCOUNT_SERVICE_URL=your_account_api_url
TICKET_SERVICE_URL=your_ticket_api_url
```

### 3. Test Locally (Optional)

If you want to test the conversation flow before deploying:

```bash
# Install watsonx Orchestrate CLI
npm install -g @ibm/watsonx-orchestrate-cli

# Login
wx-orchestrate login --apikey YOUR_API_KEY

# Test agent configuration
wx-orchestrate agent validate --file agents/customer-complaint-agent.yaml

# Test flow
wx-orchestrate flow validate --file flows/complaint-handling-flow.yaml
```

### 4. Deploy to Orchestrate

**Web Interface (Easiest):**

1. Go to https://orchestrate.ibm.com
2. Navigate to Skills → Import
3. Upload `agents/customer-complaint-agent.yaml`
4. Upload `flows/complaint-handling-flow.yaml`
5. Upload `knowledge/complaint-knowledge-base.yaml`
6. Configure integrations (tools/*.yaml)
7. Click "Deploy"

**CLI (Faster):**

```bash
# Deploy everything at once
wx-orchestrate deploy \
  --agent agents/customer-complaint-agent.yaml \
  --flow flows/complaint-handling-flow.yaml \
  --knowledge knowledge/complaint-knowledge-base.yaml \
  --tools tools/
```

### 5. Test the Agent

Start a conversation:

```
You: Hello
Agent: Hello! Thank you for contacting us today...

You: ABC12345678
Agent: Thank you. Could you please provide your full name?

You: John Smith
Agent: What email address should we use to contact you?

You: john@email.com
Agent: Thank you, John Smith. Now, please tell me about the issue...

You: I was charged twice for my subscription
Agent: I understand your concern about the billing issue...
```

## 📋 Sample Test Scenarios

### Scenario 1: Billing Issue

```
Account: ABC12345678
Name: John Smith
Email: john@email.com
Complaint: "I was charged twice for my monthly subscription"
Expected: Categorized as "billing_issue", ticket created, solutions provided
```

### Scenario 2: Service Outage

```
Account: XYZ98765432
Name: Jane Doe
Email: jane@email.com
Complaint: "My service has been down for 2 hours"
Expected: Categorized as "service_outage", high priority, immediate escalation
```

### Scenario 3: Product Defect

```
Account: DEF11223344
Name: Bob Johnson
Email: bob@email.com
Complaint: "The product I received is damaged"
Expected: Categorized as "product_defect", replacement process initiated
```

## 🧪 Testing Checklist

- [ ] Agent greets customer properly
- [ ] Account number validation works
- [ ] Email validation works
- [ ] Complaint is understood and categorized
- [ ] Knowledge base returns relevant solutions
- [ ] Ticket is created successfully
- [ ] Confirmation email is sent
- [ ] Escalation works for critical issues
- [ ] Sentiment analysis detects negative emotions
- [ ] Conversation can be ended gracefully

## 🔧 Common Issues & Quick Fixes

### Issue: "Authentication Failed"
```bash
# Solution: Refresh your API key
export WATSONX_API_KEY=new_key_here
wx-orchestrate login --apikey $WATSONX_API_KEY
```

### Issue: "Agent Not Responding"
```bash
# Solution: Check agent status
wx-orchestrate agent status customer-complaint-agent

# Restart if needed
wx-orchestrate agent restart customer-complaint-agent
```

### Issue: "Integration Error"
```bash
# Solution: Test integrations individually
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.yourcompany.com/accounts/TEST123/verify
```

### Issue: "Knowledge Base Not Found"
```bash
# Solution: Re-import knowledge base
wx-orchestrate knowledge import \
  --file knowledge/complaint-knowledge-base.yaml \
  --force
```

## 📊 Monitoring Your Test

View real-time metrics:

```bash
# Watch conversation logs
wx-orchestrate logs --agent customer-complaint-agent --follow

# Check metrics
wx-orchestrate metrics --agent customer-complaint-agent

# View recent conversations
wx-orchestrate conversations list --limit 10
```

## 🎯 Next Steps

Once basic testing is complete:

1. **Customize Responses**
   - Edit `agents/customer-complaint-agent.yaml`
   - Modify response templates
   - Add your company's tone and voice

2. **Expand Knowledge Base**
   - Add more complaint categories
   - Include company-specific solutions
   - Add FAQ entries

3. **Configure Integrations**
   - Connect to your actual account system
   - Link to your ticket management system
   - Set up email notifications

4. **Fine-tune Behavior**
   - Adjust escalation thresholds
   - Modify sentiment analysis sensitivity
   - Customize conversation flow

5. **Deploy to Production**
   - Follow the full [DEPLOYMENT.md](DEPLOYMENT.md) guide
   - Set up monitoring and alerts
   - Train your support team

## 💡 Pro Tips

1. **Start Small**: Test with a few users before full rollout
2. **Monitor Closely**: Watch the first 100 conversations carefully
3. **Iterate Quickly**: Make adjustments based on real feedback
4. **Document Changes**: Keep track of what works and what doesn't
5. **Backup Configs**: Save working configurations before making changes

## 🆘 Need Help?

- **Documentation**: See [README.md](README.md) for detailed information
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- **IBM Docs**: https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base
- **Support**: support@yourcompany.com

## 📝 Quick Reference

### Key Files
- `agents/customer-complaint-agent.yaml` - Main agent configuration
- `flows/complaint-handling-flow.yaml` - Conversation flow
- `knowledge/complaint-knowledge-base.yaml` - Solutions database
- `tools/account-lookup-tool.yaml` - Account API integration
- `tools/ticket-system-tool.yaml` - Ticket API integration

### Key Commands
```bash
# Deploy
wx-orchestrate deploy --agent agents/customer-complaint-agent.yaml

# Test
wx-orchestrate test --agent customer-complaint-agent

# Monitor
wx-orchestrate logs --agent customer-complaint-agent --follow

# Update
wx-orchestrate agent update --file agents/customer-complaint-agent.yaml
```

### Environment Variables (Minimum)
```bash
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project
ACCOUNT_SERVICE_URL=your_account_api
TICKET_SERVICE_URL=your_ticket_api
```

---

**Ready to go?** Start with step 1 and you'll have a working agent in 5 minutes! 🎉

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)