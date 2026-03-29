"""
Simple Mock CRM API for Customer Account Lookup
Can be deployed as IBM Cloud Function or run locally
"""

import json
from typing import Dict, Any, Optional

# Customer database
CUSTOMERS = [
    {
        "account_number": "ACC12345678",
        "full_name": "John Smith",
        "email": "john.smith@email.com",
        "phone": "+1-555-0101",
        "status": "active",
        "created_date": "2023-01-15",
        "account_type": "premium"
    },
    {
        "account_number": "ACC23456789",
        "full_name": "Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "+1-555-0102",
        "status": "active",
        "created_date": "2023-02-20",
        "account_type": "standard"
    },
    {
        "account_number": "ACC34567890",
        "full_name": "Michael Chen",
        "email": "michael.chen@email.com",
        "phone": "+1-555-0103",
        "status": "active",
        "created_date": "2023-03-10",
        "account_type": "premium"
    },
    {
        "account_number": "ACC45678901",
        "full_name": "Emily Davis",
        "email": "emily.davis@email.com",
        "phone": "+1-555-0104",
        "status": "active",
        "created_date": "2023-04-05",
        "account_type": "standard"
    },
    {
        "account_number": "ACC56789012",
        "full_name": "Robert Martinez",
        "email": "robert.martinez@email.com",
        "phone": "+1-555-0105",
        "status": "active",
        "created_date": "2023-05-12",
        "account_type": "premium"
    },
    {
        "account_number": "ACC67890123",
        "full_name": "Jennifer Wilson",
        "email": "jennifer.wilson@email.com",
        "phone": "+1-555-0106",
        "status": "active",
        "created_date": "2023-06-18",
        "account_type": "standard"
    },
    {
        "account_number": "ACC78901234",
        "full_name": "David Brown",
        "email": "david.brown@email.com",
        "phone": "+1-555-0107",
        "status": "active",
        "created_date": "2023-07-22",
        "account_type": "premium"
    },
    {
        "account_number": "ACC89012345",
        "full_name": "Lisa Anderson",
        "email": "lisa.anderson@email.com",
        "phone": "+1-555-0108",
        "status": "active",
        "created_date": "2023-08-30",
        "account_type": "standard"
    },
    {
        "account_number": "ACC90123456",
        "full_name": "James Taylor",
        "email": "james.taylor@email.com",
        "phone": "+1-555-0109",
        "status": "active",
        "created_date": "2023-09-14",
        "account_type": "premium"
    },
    {
        "account_number": "ACC01234567",
        "full_name": "Maria Garcia",
        "email": "maria.garcia@email.com",
        "phone": "+1-555-0110",
        "status": "active",
        "created_date": "2023-10-25",
        "account_type": "standard"
    }
]


def find_customer_by_account(account_number: str) -> Optional[Dict[str, Any]]:
    """Find a customer by account number"""
    for customer in CUSTOMERS:
        if customer["account_number"] == account_number:
            return customer
    return None


def verify_account(account_number: str) -> Dict[str, Any]:
    """Verify if an account exists"""
    customer = find_customer_by_account(account_number)
    if customer:
        return {
            "account_exists": True,
            "account_status": customer["status"],
            "account_type": customer["account_type"],
            "customer_id": account_number
        }
    return {
        "account_exists": False,
        "account_status": "not_found",
        "account_type": None,
        "customer_id": None
    }


def get_account_details(account_number: str) -> Dict[str, Any]:
    """Get full account details"""
    customer = find_customer_by_account(account_number)
    if customer:
        return {
            "success": True,
            "data": customer
        }
    return {
        "success": False,
        "error": "Account not found",
        "data": None
    }


def list_all_customers() -> Dict[str, Any]:
    """List all customers (for admin purposes)"""
    return {
        "success": True,
        "count": len(CUSTOMERS),
        "customers": CUSTOMERS
    }


# IBM Cloud Function main handler
def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main handler for IBM Cloud Function
    
    Supported operations:
    - verify: Verify if account exists
    - get_details: Get full account details
    - list_all: List all customers
    
    Example params:
    {
        "operation": "verify",
        "account_number": "ACC12345678"
    }
    """
    operation = params.get("operation", "verify")
    account_number = params.get("account_number", "")
    
    if operation == "verify":
        result = verify_account(account_number)
        return {
            "statusCode": 200 if result["account_exists"] else 404,
            "headers": {"Content-Type": "application/json"},
            "body": result
        }
    
    elif operation == "get_details":
        result = get_account_details(account_number)
        return {
            "statusCode": 200 if result["success"] else 404,
            "headers": {"Content-Type": "application/json"},
            "body": result
        }
    
    elif operation == "list_all":
        result = list_all_customers()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": result
        }
    
    else:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": {
                "success": False,
                "error": f"Unknown operation: {operation}",
                "supported_operations": ["verify", "get_details", "list_all"]
            }
        }


# For local testing
if __name__ == "__main__":
    # Test verify
    print("Testing verify operation:")
    result = main({"operation": "verify", "account_number": "ACC12345678"})
    print(json.dumps(result, indent=2))
    
    print("\nTesting get_details operation:")
    result = main({"operation": "get_details", "account_number": "ACC12345678"})
    print(json.dumps(result, indent=2))
    
    print("\nTesting account not found:")
    result = main({"operation": "verify", "account_number": "ACC99999999"})
    print(json.dumps(result, indent=2))

# Made with Bob
