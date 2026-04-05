# Lendyr Bank Orchestrator Agent

## Overview

The Lendyr Bank Orchestrator Agent is a native agent for watsonx Orchestrate that serves as the main entry point for customers accessing Lendyr Bank's digital banking services.

## Features

The orchestrator agent provides:

1. **Warm Welcome**: Greets customers professionally when they access the banking system
2. **Service Navigation**: Presents three main banking services:
   - Check account balances
   - Activate debit or credit cards
   - Transfer money
3. **Intelligent Routing**: Guides customers to the appropriate service based on their needs
4. **Security Awareness**: Maintains security best practices and reminds customers about safe banking

## File Structure

- `lendyr_bank_orchestrator.py` - Python-based agent configuration
- `README_ORCHESTRATOR.md` - This documentation file

## Agent Configuration

The agent is configured with the following key settings:

- **Name**: LendyrBankOrchestrator
- **Display Name**: Lendyr Bank Orchestrator
- **LLM**: watsonx/ibm/granite-13b-chat-v2
- **Memory**: Enabled for context retention
- **Style**: Default conversational style

## Usage

### Python Format

The agent is defined in Python format as per watsonx Orchestrate ADK specifications. To use this agent:

1. **Import the configuration**:
```python
from agents.lendyr_bank_orchestrator import get_agent_config, validate_agent_config

# Get the agent configuration
config = get_agent_config()

# Validate the configuration
if validate_agent_config():
    print("Agent configuration is valid")
```

2. **Validate the configuration**:
```bash
python agents/lendyr_bank_orchestrator.py
```

This will output:
```
✓ Agent configuration is valid
✓ Agent Name: LendyrBankOrchestrator
✓ Display Name: Lendyr Bank Orchestrator
✓ LLM: watsonx/ibm/granite-13b-chat-v2
```

### Converting to YAML

If you need to convert this Python configuration to YAML format for deployment:

```python
import yaml
from agents.lendyr_bank_orchestrator import get_agent_config

config = get_agent_config()

with open('agents/lendyr-bank-orchestrator.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
```

## Conversation Flow

### Initial Greeting
```
Agent: "Welcome to Lendyr Bank! I'm your virtual banking assistant, here to help 
you with your banking needs today. How may I assist you?"
```

### Service Menu
```
Agent: "I can help you with:
1. Check account balances
2. Activate debit or credit cards
3. Transfer money

Which service would you like to use today?"
```

### Service Routing
- **Option 1**: Guides customer through balance checking process
- **Option 2**: Guides customer through card activation process
- **Option 3**: Guides customer through money transfer process

## Security Features

The agent includes built-in security awareness:
- Never requests sensitive information (full card numbers, CVV, passwords)
- Reminds customers about safe banking practices
- Declines suspicious requests and suggests contacting customer service

## Customization

To customize the agent:

1. **Modify Instructions**: Edit the `instructions` field in `agent_config`
2. **Add Tools**: Add tool configurations to the `tools` array
3. **Add Knowledge Base**: Configure the `knowledge_base` array
4. **Adjust LLM**: Change the `llm` field to use a different model

## Integration with Other Agents

This orchestrator can work with specialized agents:
- **Account Balance Agent**: For detailed balance inquiries
- **Card Activation Agent**: For card activation workflows
- **Transfer Agent**: For money transfer operations

## Deployment

To deploy this agent to watsonx Orchestrate:

1. Ensure you have the watsonx Orchestrate ADK installed
2. Convert the Python configuration to the required format (YAML/JSON)
3. Upload to your watsonx Orchestrate instance
4. Test the agent in the Orchestrate environment

## Testing

Test the agent configuration:

```bash
# Validate configuration
python agents/lendyr_bank_orchestrator.py

# Expected output:
# ✓ Agent configuration is valid
# ✓ Agent Name: LendyrBankOrchestrator
# ✓ Display Name: Lendyr Bank Orchestrator
# ✓ LLM: watsonx/ibm/granite-13b-chat-v2
```

## Support

For issues or questions about this agent:
- Review the watsonx Orchestrate ADK documentation
- Check the agent configuration for proper formatting
- Ensure all required fields are present

## Version

- **Spec Version**: v1
- **Created**: 2026-04-05
- **Format**: Python (watsonx Orchestrate ADK)