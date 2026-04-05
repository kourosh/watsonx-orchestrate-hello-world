# Quick Start Guide - Lendyr Bank Orchestrator Agent

## Overview

This guide will help you quickly get started with the Lendyr Bank Orchestrator Agent, a Python-based native agent for watsonx Orchestrate.

## What Does This Agent Do?

The Lendyr Bank Orchestrator Agent:
- ✅ Welcomes users to Lendyr Bank
- ✅ Presents three main banking services
- ✅ Routes customers to the appropriate service
- ✅ Maintains security best practices

## Files Created

1. **`lendyr_bank_orchestrator.py`** - Python agent configuration (main file)
2. **`lendyr-bank-orchestrator.yaml`** - YAML version for deployment
3. **`convert_to_yaml.py`** - Conversion utility script
4. **`README_ORCHESTRATOR.md`** - Detailed documentation
5. **`QUICKSTART_ORCHESTRATOR.md`** - This quick start guide

## Quick Test

### 1. Validate the Python Configuration

```bash
cd agents
python3 lendyr_bank_orchestrator.py
```

**Expected Output:**
```
✓ Agent configuration is valid
✓ Agent Name: LendyrBankOrchestrator
✓ Display Name: Lendyr Bank Orchestrator
✓ LLM: watsonx/ibm/granite-13b-chat-v2
```

### 2. Generate YAML for Deployment

```bash
cd agents
python3 convert_to_yaml.py
```

**Expected Output:**
```
✓ Successfully converted agent configuration to YAML
✓ Output file: /path/to/agents/lendyr-bank-orchestrator.yaml
✓ Agent Name: LendyrBankOrchestrator
✓ Display Name: Lendyr Bank Orchestrator
```

## Agent Conversation Flow

### Example Interaction

**User:** Hi

**Agent:** Welcome to Lendyr Bank! I'm your virtual banking assistant, here to help you with your banking needs today. How may I assist you?

**User:** What can you help me with?

**Agent:** I can help you with:
1. Check account balances
2. Activate debit or credit cards
3. Transfer money

Which service would you like to use today?

**User:** I want to check my balance

**Agent:** Great! I'll help you check your account balance. [Proceeds with balance checking flow]

## Service Options

### 1. Check Account Balances
- View checking account balances
- View savings account balances
- View credit card balances
- Review recent transactions

### 2. Activate Debit or Credit Cards
- Activate new debit cards
- Activate new credit cards
- Verify card information
- Set up card PINs

### 3. Transfer Money
- Transfer between your own accounts
- Send money to other Lendyr Bank customers
- Set up external transfers
- Schedule recurring transfers

## Deployment to watsonx Orchestrate

### Option 1: Using YAML File

1. Upload `lendyr-bank-orchestrator.yaml` to your watsonx Orchestrate instance
2. Navigate to the Agents section
3. Import the YAML file
4. Test the agent in the Orchestrate environment

### Option 2: Using Python Configuration

1. Use the watsonx Orchestrate ADK to import the Python configuration
2. Import the `lendyr_bank_orchestrator` module
3. Deploy using the ADK deployment tools

```python
from agents.lendyr_bank_orchestrator import get_agent_config

config = get_agent_config()
# Deploy using watsonx Orchestrate ADK
```

## Customization

### Modify the Greeting

Edit the `instructions` field in `lendyr_bank_orchestrator.py`:

```python
"instructions": """You are the Lendyr Bank Orchestrator Agent...

GREETING AND WELCOME:
When a customer first interacts with you, greet them warmly:
"[Your custom greeting here]"
...
"""
```

### Add More Services

Add additional service options to the instructions:

```python
4. **New Service Name**
   - Service feature 1
   - Service feature 2
```

### Change the LLM Model

Modify the `llm` field:

```python
"llm": "watsonx/ibm/granite-20b-chat-v2",  # Use a different model
```

## Integration with Other Agents

This orchestrator can delegate to specialized agents:

```python
"collaborators": [
    "AccountBalanceAgent",
    "CardActivationAgent", 
    "TransferAgent"
]
```

## Troubleshooting

### Issue: Python command not found
**Solution:** Use `python3` instead of `python`

### Issue: Module import error
**Solution:** Ensure you're running from the `agents` directory

### Issue: YAML conversion fails
**Solution:** Check that PyYAML is installed: `pip3 install pyyaml`

## Next Steps

1. ✅ Test the agent configuration
2. ✅ Generate the YAML file
3. ⬜ Deploy to watsonx Orchestrate
4. ⬜ Test in the Orchestrate environment
5. ⬜ Integrate with specialized agents
6. ⬜ Add tools and knowledge bases as needed

## Support

For more information:
- See `README_ORCHESTRATOR.md` for detailed documentation
- Review the watsonx Orchestrate ADK documentation
- Check the agent configuration in `lendyr_bank_orchestrator.py`

## Summary

You now have a fully functional Lendyr Bank Orchestrator Agent that:
- Welcomes customers professionally
- Offers three main banking services
- Routes customers appropriately
- Maintains security best practices

The agent is ready to deploy to watsonx Orchestrate!