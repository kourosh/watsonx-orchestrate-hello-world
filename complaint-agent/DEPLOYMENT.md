# Deployment Guide - Customer Complaint Agent

This guide provides step-by-step instructions for deploying the Customer Complaint Agent to IBM watsonx Orchestrate.

## Prerequisites

Before deploying, ensure you have:

- [ ] IBM watsonx Orchestrate account with admin access
- [ ] watsonx.ai access with Granite model availability
- [ ] API credentials for account lookup service
- [ ] API credentials for ticket management system
- [ ] SMTP credentials for email notifications (optional)
- [ ] watsonx Orchestrate CLI installed (optional but recommended)

## Deployment Steps

### Step 1: Prepare Environment

1. **Clone or download the agent files**
   ```bash
   cd /path/to/complaint-agent
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

3. **Verify file structure**
   ```bash
   tree .
   # Should show:
   # ├── agents/
   # ├── flows/
   # ├── knowledge/
   # ├── tools/
   # ├── README.md
   # ├── DEPLOYMENT.md
   # └── .env.example
   ```

### Step 2: Set Up watsonx.ai Model

1. **Log in to watsonx.ai**
   - Navigate to https://dataplatform.cloud.ibm.com/wx/home

2. **Create or select a project**
   - Go to Projects → Create new project
   - Name: "Customer Complaint Agent"
   - Select appropriate storage

3. **Configure Granite model**
   - Navigate to Foundation models
   - Select `ibm/granite-13b-chat-v2`
   - Note the model ID and deployment details

4. **Generate API credentials**
   - Go to Profile → API Keys
   - Create new API key
   - Save the key securely
   - Update `WATSONX_API_KEY` in your .env file

### Step 3: Deploy to watsonx Orchestrate

#### Option A: Using the Web Interface

1. **Access watsonx Orchestrate**
   - Navigate to https://orchestrate.ibm.com
   - Log in with your IBM Cloud credentials

2. **Create a new skill**
   - Go to Skills → Create skill
   - Select "Import from file"
   - Upload `agents/customer-complaint-agent.yaml`

3. **Configure the agent**
   - Set the display name: "Customer Complaint Agent"
   - Add description from the YAML file
   - Configure model settings:
     - Model: granite-13b-chat-v2
     - Temperature: 0.7
     - Max tokens: 2048

4. **Import conversation flow**
   - Go to Flows → Import flow
   - Upload `flows/complaint-handling-flow.yaml`
   - Link flow to the agent skill

5. **Set up knowledge base**
   - Go to Knowledge → Import
   - Upload `knowledge/complaint-knowledge-base.yaml`
   - Index the knowledge base
   - Link to agent

6. **Configure tools/integrations**
   - Go to Integrations → Add integration
   - For Account Lookup:
     - Upload `tools/account-lookup-tool.yaml`
     - Configure OAuth2 credentials
     - Test connection
   - For Ticket System:
     - Upload `tools/ticket-system-tool.yaml`
     - Configure API key
     - Test connection

#### Option B: Using the CLI

1. **Install watsonx Orchestrate CLI**
   ```bash
   npm install -g @ibm/watsonx-orchestrate-cli
   ```

2. **Authenticate**
   ```bash
   wx-orchestrate login --apikey YOUR_API_KEY
   ```

3. **Deploy agent**
   ```bash
   wx-orchestrate agent deploy \
     --file agents/customer-complaint-agent.yaml \
     --workspace YOUR_WORKSPACE_ID
   ```

4. **Deploy flow**
   ```bash
   wx-orchestrate flow deploy \
     --file flows/complaint-handling-flow.yaml \
     --agent customer-complaint-agent
   ```

5. **Deploy knowledge base**
   ```bash
   wx-orchestrate knowledge import \
     --file knowledge/complaint-knowledge-base.yaml \
     --agent customer-complaint-agent
   ```

6. **Deploy tools**
   ```bash
   wx-orchestrate tool deploy \
     --file tools/account-lookup-tool.yaml
   
   wx-orchestrate tool deploy \
     --file tools/ticket-system-tool.yaml
   ```

### Step 4: Configure Integrations

#### Account Lookup Service

1. **Set up OAuth2 authentication**
   - Client ID: From your account service provider
   - Client Secret: From your account service provider
   - Token URL: Your OAuth2 token endpoint
   - Scopes: `account:read`

2. **Test the integration**
   ```bash
   curl -X GET \
     -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.yourcompany.com/accounts/TEST123/verify
   ```

3. **Configure in Orchestrate**
   - Go to Integrations → Account Lookup
   - Add OAuth2 credentials
   - Test with a sample account number
   - Verify response format matches expected schema

#### Ticket System

1. **Set up API key authentication**
   - Generate API key from your ticket system
   - Add to environment variables
   - Configure rate limits if applicable

2. **Test the integration**
   ```bash
   curl -X POST \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"account_number":"TEST123","category":"test"}' \
     https://api.yourcompany.com/tickets
   ```

3. **Configure in Orchestrate**
   - Go to Integrations → Ticket System
   - Add API key
   - Test ticket creation
   - Verify ticket ID is returned

### Step 5: Test the Agent

#### Unit Testing

1. **Test greeting flow**
   - Start a new conversation
   - Verify greeting message appears
   - Check for proper formatting

2. **Test account collection**
   - Provide valid account number
   - Verify validation works
   - Test invalid format handling
   - Confirm retry logic (max 3 attempts)

3. **Test complaint processing**
   - Submit various complaint types
   - Verify categorization accuracy
   - Check knowledge base search results
   - Confirm ticket creation

4. **Test error handling**
   - Invalid account number
   - Service unavailable scenarios
   - Network timeout situations
   - Malformed input data

#### Integration Testing

1. **End-to-end flow test**
   ```
   User: Hello
   Agent: [Greeting]
   User: ABC12345678
   Agent: [Account verification]
   User: John Smith
   Agent: [Name confirmation]
   User: john@email.com
   Agent: [Email confirmation]
   User: I was charged twice
   Agent: [Complaint processing]
   [Ticket created]
   Agent: [Summary and next steps]
   ```

2. **Verify integrations**
   - Account lookup returns correct data
   - Tickets are created in the system
   - Emails are sent to customers
   - Knowledge base returns relevant articles

3. **Test escalation scenarios**
   - Critical severity complaints
   - Negative sentiment detection
   - High-value billing issues
   - Repeat customer complaints

### Step 6: Configure Monitoring

1. **Set up logging**
   - Configure log aggregation
   - Set log retention policies
   - Create log alerts for errors

2. **Configure metrics**
   - Conversation duration
   - Customer satisfaction scores
   - Ticket creation rate
   - Escalation rate
   - SLA compliance

3. **Set up dashboards**
   - Real-time conversation monitoring
   - Daily/weekly reports
   - Performance metrics
   - Error tracking

4. **Configure alerts**
   - High error rate (> 5%)
   - Low satisfaction score (< 3.0)
   - SLA violations
   - Service downtime

### Step 7: Production Deployment

1. **Review configuration**
   - [ ] All environment variables set
   - [ ] Integrations tested and working
   - [ ] Knowledge base indexed
   - [ ] Monitoring configured
   - [ ] Alerts set up

2. **Gradual rollout**
   - Start with 10% of traffic
   - Monitor for 24 hours
   - Increase to 50% if stable
   - Full rollout after 48 hours

3. **Create rollback plan**
   - Document current configuration
   - Prepare fallback to human agents
   - Test rollback procedure
   - Define rollback triggers

4. **Go live**
   - Enable agent in production
   - Monitor closely for first 24 hours
   - Be ready to intervene if needed
   - Collect feedback from users

## Post-Deployment

### Week 1: Intensive Monitoring

- [ ] Monitor all conversations
- [ ] Review categorization accuracy
- [ ] Check escalation patterns
- [ ] Analyze customer feedback
- [ ] Adjust thresholds as needed

### Week 2-4: Optimization

- [ ] Fine-tune response templates
- [ ] Expand knowledge base
- [ ] Optimize conversation flow
- [ ] Improve categorization model
- [ ] Reduce escalation rate

### Ongoing Maintenance

- [ ] Weekly performance reviews
- [ ] Monthly knowledge base updates
- [ ] Quarterly model retraining
- [ ] Regular security audits
- [ ] Continuous improvement based on feedback

## Troubleshooting

### Agent Not Responding

**Symptoms:** Agent doesn't reply to user messages

**Solutions:**
1. Check API connectivity
2. Verify authentication tokens are valid
3. Review error logs
4. Restart the agent service
5. Check rate limits

### Incorrect Categorization

**Symptoms:** Complaints categorized incorrectly

**Solutions:**
1. Review training examples
2. Add more keywords to categories
3. Adjust classification confidence threshold
4. Retrain the model with more data
5. Add manual override rules

### High Escalation Rate

**Symptoms:** Too many conversations escalated to humans

**Solutions:**
1. Review escalation thresholds
2. Expand knowledge base coverage
3. Improve response quality
4. Add more self-service options
5. Train model on resolved cases

### Integration Failures

**Symptoms:** API calls failing

**Solutions:**
1. Verify credentials are current
2. Check API endpoint availability
3. Review rate limits
4. Implement retry logic
5. Add circuit breaker pattern

## Security Considerations

1. **Data Protection**
   - Encrypt sensitive data at rest
   - Use TLS for all API calls
   - Implement data retention policies
   - Regular security audits

2. **Access Control**
   - Use role-based access control (RBAC)
   - Implement least privilege principle
   - Regular credential rotation
   - Multi-factor authentication

3. **Compliance**
   - GDPR compliance for EU customers
   - CCPA compliance for California
   - PCI DSS for payment data
   - Regular compliance audits

## Support

For deployment issues:
- Email: devops@yourcompany.com
- Slack: #watsonx-orchestrate-support
- Documentation: https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base

## Rollback Procedure

If issues arise:

1. **Immediate actions**
   ```bash
   wx-orchestrate agent disable customer-complaint-agent
   ```

2. **Route to human agents**
   - Enable fallback routing
   - Notify support team
   - Monitor queue depth

3. **Investigate and fix**
   - Review error logs
   - Identify root cause
   - Apply fixes
   - Test in staging

4. **Redeploy**
   - Deploy fixed version
   - Gradual rollout again
   - Monitor closely

---

**Deployment Checklist**

- [ ] Environment configured
- [ ] watsonx.ai model set up
- [ ] Agent deployed
- [ ] Flow deployed
- [ ] Knowledge base imported
- [ ] Tools configured
- [ ] Integrations tested
- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] Team trained
- [ ] Documentation updated
- [ ] Rollback plan ready
- [ ] Go-live approved

**Deployment Date:** _______________

**Deployed By:** _______________

**Approved By:** _______________