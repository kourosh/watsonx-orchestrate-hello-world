# Customer Complaint Agent for watsonx Orchestrate

A comprehensive orchestrator agent built for IBM watsonx Orchestrate that handles customer complaints through an automated, empathetic, and efficient workflow.

## Overview

This agent provides a complete customer complaint handling solution that:
- **Greets customers** warmly and professionally
- **Collects account information** systematically
- **Understands complaints** through natural language processing
- **Categorizes issues** automatically
- **Creates support tickets** with proper routing
- **Provides solutions** from a knowledge base
- **Escalates when necessary** based on severity and sentiment

## Architecture

```
complaint-agent/
├── agents/
│   └── customer-complaint-agent.yaml       # Main agent configuration
├── flows/
│   └── complaint-handling-flow.yaml        # Orchestrated conversation flow
├── knowledge/
│   └── complaint-knowledge-base.yaml       # Solutions and FAQ database
├── tools/
│   ├── account-lookup-tool.yaml            # Account verification API
│   └── ticket-system-tool.yaml             # Ticket management API
└── README.md                                # This file
```

## Features

### 1. Intelligent Greeting
- Warm, professional introduction
- Sets expectations for the interaction
- Establishes rapport with the customer

### 2. Account Information Collection
The agent systematically collects:
- **Account Number** (validated format: 8-12 alphanumeric characters)
- **Customer Name** (verified against account)
- **Contact Email** (validated email format)
- **Contact Phone** (optional)

### 3. Complaint Understanding
- Natural language processing to understand the issue
- Probing questions for additional details
- Context gathering (when, frequency, impact)
- Sentiment analysis throughout the conversation

### 4. Automatic Categorization
Complaints are automatically categorized into:
- Billing Issues
- Service Outages
- Product Defects
- Account Access Problems
- Technical Support
- General Inquiries
- Other

### 5. Knowledge Base Integration
- Searches for relevant solutions
- Provides immediate answers when available
- References similar resolved cases
- Offers self-service options

### 6. Ticket Management
- Creates detailed support tickets
- Assigns appropriate priority and severity
- Routes to specialized teams
- Tracks SLA compliance
- Sends confirmation emails

### 7. Smart Escalation
Automatic escalation triggers:
- Critical severity issues
- Negative customer sentiment (< -0.7)
- High-value billing disputes (> $500)
- Repeat complaints
- SLA violations

## Configuration

### Environment Variables

Set the following environment variables before deploying:

```bash
# Account Service
ACCOUNT_SERVICE_URL=https://api.yourcompany.com/accounts
AUTH_TOKEN_URL=https://auth.yourcompany.com/oauth/token
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret

# Ticket Service
TICKET_SERVICE_URL=https://api.yourcompany.com/tickets
TICKET_API_KEY=your_ticket_api_key
```

### watsonx Orchestrate Setup

1. **Import the Agent**
   ```bash
   # Upload customer-complaint-agent.yaml to watsonx Orchestrate
   ```

2. **Configure Skills**
   - Enable conversational AI model (Granite 13B recommended)
   - Connect account lookup API
   - Connect ticket system API
   - Import knowledge base

3. **Set Up Integrations**
   - Configure OAuth2 for account service
   - Configure API key for ticket service
   - Test connectivity for all endpoints

4. **Deploy Flow**
   - Import complaint-handling-flow.yaml
   - Map flow states to agent skills
   - Configure state transitions
   - Test end-to-end flow

## Usage

### Starting a Conversation

The agent automatically initiates with a greeting when a customer interaction begins:

```
Agent: "Hello! Thank you for contacting us today. I'm here to help you with 
any concerns. Before we begin, I'll need to collect some information to 
better assist you."
```

### Example Conversation Flow

```
Agent: May I have your account number, please?
Customer: ABC12345678

Agent: Thank you. Could you please provide your full name?
Customer: John Smith

Agent: What email address should we use to contact you?
Customer: john.smith@email.com

Agent: Thank you, John Smith. I have your information. Now, please tell me 
about the issue you're experiencing.

Customer: I was charged twice for my subscription this month.

Agent: I understand your concern about the billing issue. To help you better, 
could you please provide:
- When did you notice the duplicate charge?
- What is the amount of each charge?

Customer: I noticed it yesterday. Each charge is $49.99.

Agent: Thank you for providing all this information, John Smith.

Here's a summary of your complaint:
- Category: Billing Issue
- Severity: Medium
- Ticket ID: TKT-2024-001234

Based on similar cases, here are some potential solutions:
1. Verify if one charge is for the current month and one for next month
2. Check if you have multiple active subscriptions

What happens next:
1. Your complaint has been logged and assigned to our billing team
2. You'll receive a confirmation email at john.smith@email.com within 15 minutes
3. Our team will review your case and contact you within 24-48 hours
4. You can track your ticket status using ID: TKT-2024-001234

Is there anything else I can help you with today?
```

## Conversation States

The flow includes the following states:

1. **greeting** - Initial welcome message
2. **collect_account_number** - Gather account ID
3. **verify_account** - Validate account exists
4. **collect_customer_name** - Get customer name
5. **collect_contact_email** - Get email address
6. **collect_contact_phone** - Get phone (optional)
7. **account_info_summary** - Confirm collected data
8. **collect_complaint** - Listen to the issue
9. **ask_for_more_details** - Gather additional context
10. **collect_additional_details** - Capture extra information
11. **analyze_complaint** - Categorize and assess severity
12. **search_knowledge_base** - Find relevant solutions
13. **create_ticket** - Generate support ticket
14. **provide_summary_and_next_steps** - Communicate resolution plan
15. **ask_additional_help** - Check for more issues
16. **closing** - End conversation gracefully

## Error Handling

The agent handles various error scenarios:

### Account Not Found
- Allows 3 retry attempts
- Offers to transfer to account services
- Logs failed verification attempts

### Invalid Input
- Provides clear validation messages
- Suggests correct format
- Offers examples

### Service Unavailable
- Implements retry with exponential backoff
- Queues requests when service is down
- Escalates to human agent if persistent

### Negative Sentiment
- Monitors sentiment throughout conversation
- Escalates to supervisor if sentiment < -0.7
- Adjusts tone and offers immediate assistance

## Knowledge Base

The knowledge base includes solutions for:

### Billing Issues
- Unexpected charges
- Payment not reflected
- Incorrect amounts

### Service Outages
- Complete outages
- Intermittent issues
- Performance problems

### Product Defects
- Malfunctions
- Damaged products
- Missing parts

### Account Access
- Login problems
- Locked accounts
- Feature restrictions

### Technical Support
- Error messages
- Integration issues
- Compatibility problems

## Monitoring & Analytics

The agent tracks:

- **Conversation Metrics**
  - Average conversation duration
  - Completion rate
  - Abandonment rate

- **Customer Satisfaction**
  - Sentiment scores
  - Resolution satisfaction
  - NPS scores

- **Operational Metrics**
  - Ticket creation rate
  - Category distribution
  - Escalation rate
  - SLA compliance

- **Quality Metrics**
  - Information collection completeness
  - Categorization accuracy
  - First contact resolution rate

## Customization

### Adding New Complaint Categories

Edit `knowledge/complaint-knowledge-base.yaml`:

```yaml
categories:
  - id: new_category
    name: New Category Name
    description: Description of the category
    articles:
      - id: new_001
        title: Solution Title
        keywords: [keyword1, keyword2]
        solution: |
          Step-by-step solution
        resolution_time: X business days
```

### Modifying Response Templates

Edit `agents/customer-complaint-agent.yaml`:

```yaml
response_templates:
  custom_template: |
    Your custom message with {variables}
```

### Adjusting Escalation Rules

Edit `knowledge/complaint-knowledge-base.yaml`:

```yaml
escalation_rules:
  - condition: your_condition
    action: escalation_action
    target: team_name
```

## Best Practices

1. **Always Validate Input**
   - Use regex patterns for structured data
   - Provide clear error messages
   - Limit retry attempts

2. **Show Empathy**
   - Acknowledge customer frustration
   - Use empathy statements
   - Avoid defensive language

3. **Be Transparent**
   - Set clear expectations
   - Provide realistic timelines
   - Explain next steps

4. **Maintain Context**
   - Reference previous interactions
   - Carry information through states
   - Avoid asking for same information twice

5. **Monitor Sentiment**
   - Track emotional tone
   - Escalate when negative
   - Adjust responses accordingly

## Troubleshooting

### Agent Not Responding
- Check API connectivity
- Verify authentication tokens
- Review error logs

### Incorrect Categorization
- Review training data
- Adjust classification model
- Add more examples to knowledge base

### High Escalation Rate
- Review escalation thresholds
- Improve knowledge base coverage
- Enhance agent responses

## Support

For issues or questions:
- Email: support@yourcompany.com
- Documentation: https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base
- Community: watsonx Orchestrate forums

## Version History

- **1.0.0** (2024-03-29)
  - Initial release
  - Core complaint handling flow
  - Knowledge base with 6 categories
  - Account and ticket system integration
  - Sentiment-based escalation

## License

Copyright © 2024 Your Company. All rights reserved.

## Contributing

To contribute improvements:
1. Test changes thoroughly
2. Update documentation
3. Follow YAML formatting standards
4. Submit for review

---

Built with ❤️ for watsonx Orchestrate