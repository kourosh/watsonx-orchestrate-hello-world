"""
Flask REST API for Mock CRM
Can be deployed to IBM Cloud Code Engine or run locally
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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


def find_customer_by_account(account_number):
    """Find a customer by account number"""
    for customer in CUSTOMERS:
        if customer["account_number"] == account_number:
            return customer
    return None


@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        "service": "Mock CRM API",
        "version": "1.0.0",
        "endpoints": {
            "verify_account": "GET /api/v1/accounts/{account_number}/verify",
            "get_account": "GET /api/v1/accounts/{account_number}",
            "list_customers": "GET /api/v1/customers"
        }
    })


@app.route('/api/v1/accounts/<account_number>/verify', methods=['GET'])
def verify_account(account_number):
    """Verify if an account exists"""
    customer = find_customer_by_account(account_number)
    
    if customer:
        return jsonify({
            "account_exists": True,
            "account_status": customer["status"],
            "account_type": customer["account_type"],
            "customer_id": account_number
        }), 200
    
    return jsonify({
        "account_exists": False,
        "account_status": "not_found",
        "account_type": None,
        "customer_id": None
    }), 404


@app.route('/api/v1/accounts/<account_number>', methods=['GET'])
def get_account(account_number):
    """Get full account details"""
    customer = find_customer_by_account(account_number)
    
    if customer:
        return jsonify(customer), 200
    
    return jsonify({
        "error": "Account not found",
        "account_number": account_number
    }), 404


@app.route('/api/v1/customers', methods=['GET'])
def list_customers():
    """List all customers"""
    return jsonify({
        "count": len(CUSTOMERS),
        "customers": CUSTOMERS
    }), 200


@app.route('/api/v1/customers/search', methods=['GET'])
def search_customers():
    """Search customers by name or email"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({
            "error": "Query parameter 'q' is required"
        }), 400
    
    results = []
    for customer in CUSTOMERS:
        if (query in customer["full_name"].lower() or 
            query in customer["email"].lower()):
            results.append(customer)
    
    return jsonify({
        "count": len(results),
        "customers": results
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "customers_count": len(CUSTOMERS)
    }), 200


if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)

# Made with Bob
