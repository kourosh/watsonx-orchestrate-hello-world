"""
Lendyr Bank Orchestrator Agent
A native agent for watsonx Orchestrate that welcomes users and routes them to banking services.
"""

from typing import Dict, Any

# Agent Configuration
agent_config: Dict[str, Any] = {
    "kind": "native",
    "name": "LendyrBankOrchestrator",
    "display_name": "Lendyr Bank Orchestrator",
    "description": "An orchestrator agent that welcomes customers to Lendyr Bank and helps them navigate banking services",
    "context_access_enabled": True,
    "context_variables": [],
    "restrictions": "editable",
    "memory_enabled": True,
    "llm": "watsonx/ibm/granite-13b-chat-v2",
    "style": "default",
    "hide_reasoning": False,
    "instructions": """You are the Lendyr Bank Orchestrator Agent. Your role is to welcome customers and help them navigate our banking services.

GREETING AND WELCOME:
When a customer first interacts with you, greet them warmly:
"Welcome to Lendyr Bank! I'm your virtual banking assistant, here to help you with your banking needs today. How may I assist you?"

AVAILABLE SERVICES:
You can help customers with the following services:

1. **Check Account Balances**
   - View checking account balances
   - View savings account balances
   - View credit card balances
   - Review recent transactions

2. **Activate Debit or Credit Cards**
   - Activate new debit cards
   - Activate new credit cards
   - Verify card information
   - Set up card PINs

3. **Transfer Money**
   - Transfer between your own accounts
   - Send money to other Lendyr Bank customers
   - Set up external transfers
   - Schedule recurring transfers

INTERACTION GUIDELINES:
- Always be professional, friendly, and helpful
- Present the three main service options clearly
- Ask clarifying questions to understand the customer's needs
- Guide customers step-by-step through their chosen service
- Confirm actions before executing them
- Provide clear next steps and confirmations

MENU PRESENTATION:
When presenting options, use this format:
"I can help you with:
1. Check account balances
2. Activate debit or credit cards
3. Transfer money

Which service would you like to use today?"

ROUTING LOGIC:
- If customer selects option 1: Guide them through balance checking
- If customer selects option 2: Guide them through card activation
- If customer selects option 3: Guide them through money transfer
- If customer is unsure: Ask clarifying questions about their needs
- If customer needs something else: Politely explain available services and offer alternatives

SECURITY REMINDERS:
- Never ask for full card numbers, CVV codes, or passwords
- Remind customers that Lendyr Bank will never ask for sensitive information via chat
- If a request seems suspicious, politely decline and suggest contacting customer service

Always maintain a helpful, professional tone and ensure customers feel supported throughout their banking experience.
""",
    "guidelines": [],
    "collaborators": [],
    "tools": [],
    "toolkits": [],
    "plugins": {
        "agent_pre_invoke": [],
        "agent_post_invoke": []
    },
    "knowledge_base": [],
    "chat_with_docs": {
        "enabled": False,
        "supports_full_document": True,
        "vector_index": {
            "chunk_size": 400,
            "chunk_overlap": 50,
            "limit": 10,
            "extraction_strategy": "express"
        },
        "generation": {
            "prompt_instruction": "",
            "max_docs_passed_to_llm": 5,
            "generated_response_length": "Moderate",
            "display_text_no_results_found": "I searched my knowledge base, but did not find anything related to your query",
            "display_text_connectivity_issue": "I might have information related to your query to share, but am unable to connect to my knowledge base at the moment",
            "idk_message": "I'm afraid I don't understand. Please rephrase your question.",
            "enabled": False
        },
        "query_rewrite": {
            "enabled": True
        },
        "confidence_thresholds": {
            "retrieval_confidence_threshold": "Lowest",
            "response_confidence_threshold": "Lowest"
        },
        "citations": {
            "citation_title": "How do we know?",
            "citations_shown": -1
        },
        "hap_filtering": {
            "output": {
                "enabled": False,
                "threshold": 0.5
            }
        },
        "query_source": "Agent",
        "agent_query_description": "The query to search for in the knowledge base"
    },
    "spec_version": "v1"
}


def get_agent_config() -> Dict[str, Any]:
    """
    Returns the agent configuration dictionary.
    
    Returns:
        Dict[str, Any]: The complete agent configuration
    """
    return agent_config


def validate_agent_config() -> bool:
    """
    Validates that all required fields are present in the agent configuration.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    required_fields = [
        "kind", "name", "display_name", "description", 
        "llm", "instructions", "spec_version"
    ]
    
    for field in required_fields:
        if field not in agent_config:
            print(f"Missing required field: {field}")
            return False
    
    return True


if __name__ == "__main__":
    # Validate configuration when run directly
    if validate_agent_config():
        print("✓ Agent configuration is valid")
        print(f"✓ Agent Name: {agent_config['name']}")
        print(f"✓ Display Name: {agent_config['display_name']}")
        print(f"✓ LLM: {agent_config['llm']}")
    else:
        print("✗ Agent configuration is invalid")

# Made with Bob
