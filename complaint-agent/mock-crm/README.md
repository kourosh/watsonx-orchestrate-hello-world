# Mock CRM API for Customer Complaint Agent Demo

A simple customer database API for testing the Customer Complaint Agent without needing a real CRM system.

## Customer Database

The mock CRM contains 10 test customers:

| Account Number | Full Name | Email | Phone | Account Type |
|---------------|-----------|-------|-------|--------------|
| ACC12345678 | John Smith | john.smith@email.com | +1-555-0101 | Premium |
| ACC23456789 | Sarah Johnson | sarah.johnson@email.com | +1-555-0102 | Standard |
| ACC34567890 | Michael Chen | michael.chen@email.com | +1-555-0103 | Premium |
| ACC45678901 | Emily Davis | emily.davis@email.com | +1-555-0104 | Standard |
| ACC56789012 | Robert Martinez | robert.martinez@email.com | +1-555-0105 | Premium |
| ACC67890123 | Jennifer Wilson | jennifer.wilson@email.com | +1-555-0106 | Standard |
| ACC78901234 | David Brown | david.brown@email.com | +1-555-0107 | Premium |
| ACC89012345 | Lisa Anderson | lisa.anderson@email.com | +1-555-0108 | Standard |
| ACC90123456 | James Taylor | james.taylor@email.com | +1-555-0109 | Premium |
| ACC01234567 | Maria Garcia | maria.garcia@email.com | +1-555-0110 | Standard |

## API Endpoints

### 1. Verify Account
```
GET /api/v1/accounts/{account_number}/verify
```

**Example:**
```bash
curl http://localhost:8080/api/v1/accounts/ACC12345678/verify
```

**Response:**
```json
{
  "account_exists": true,
  "account_status": "active",
  "account_type": "premium",
  "customer_id": "ACC12345678"
}
```

### 2. Get Account Details
```
GET /api/v1/accounts/{account_number}
```

**Example:**
```bash
curl http://localhost:8080/api/v1/accounts/ACC12345678
```

**Response:**
```json
{
  "account_number": "ACC12345678",
  "full_name": "John Smith",
  "email": "john.smith@email.com",
  "phone": "+1-555-0101",
  "status": "active",
  "created_date": "2023-01-15",
  "account_type": "premium"
}
```

### 3. List All Customers
```
GET /api/v1/customers
```

**Example:**
```bash
curl http://localhost:8080/api/v1/customers
```

### 4. Search Customers
```
GET /api/v1/customers/search?q={query}
```

**Example:**
```bash
curl http://localhost:8080/api/v1/customers/search?q=john
```

## Deployment Options

### Option 1: Run Locally (Quickest for Demo)

1. **Install dependencies:**
   ```bash
   cd mock-crm
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   python flask_api.py
   ```

3. **Test it:**
   ```bash
   curl http://localhost:8080/api/v1/accounts/ACC12345678/verify
   ```

The API will be available at `http://localhost:8080`

### Option 2: Deploy to IBM Cloud Code Engine

1. **Login to IBM Cloud:**
   ```bash
   ibmcloud login
   ibmcloud target --cf
   ```

2. **Create a Code Engine project:**
   ```bash
   ibmcloud ce project create --name mock-crm-api
   ibmcloud ce project select --name mock-crm-api
   ```

3. **Deploy the application:**
   ```bash
   ibmcloud ce application create \
     --name mock-crm-api \
     --build-source . \
     --port 8080 \
     --min-scale 1 \
     --max-scale 2
   ```

4. **Get the URL:**
   ```bash
   ibmcloud ce application get --name mock-crm-api
   ```

### Option 3: Deploy to IBM Cloud Functions

1. **Create the action:**
   ```bash
   ibmcloud fn action create mock-crm-api crm_api.py --web true
   ```

2. **Get the URL:**
   ```bash
   ibmcloud fn action get mock-crm-api --url
   ```

3. **Test it:**
   ```bash
   curl -X POST https://YOUR_FUNCTION_URL \
     -H "Content-Type: application/json" \
     -d '{"operation": "verify", "account_number": "ACC12345678"}'
   ```

### Option 4: Deploy to Heroku (Alternative)

1. **Create a Procfile:**
   ```
   web: gunicorn flask_api:app
   ```

2. **Deploy:**
   ```bash
   heroku create mock-crm-api
   git push heroku main
   ```

## Using with watsonx Orchestrate

Once deployed, update your agent's tool configuration:

1. **Update the account lookup tool** (`tools/account-lookup-tool.yaml`):
   ```yaml
   api:
     base_url: "http://your-api-url:8080"  # or your IBM Cloud URL
   ```

2. **Test the integration:**
   ```bash
   curl http://your-api-url:8080/api/v1/accounts/ACC12345678/verify
   ```

3. **Configure in Orchestrate:**
   - Go to your agent settings
   - Add the API endpoint
   - Test with one of the sample account numbers

## Testing the API

### Test Script

```bash
#!/bin/bash

API_URL="http://localhost:8080"

echo "Testing Mock CRM API..."
echo ""

echo "1. Health Check:"
curl -s $API_URL/health | jq
echo ""

echo "2. Verify Account (exists):"
curl -s $API_URL/api/v1/accounts/ACC12345678/verify | jq
echo ""

echo "3. Verify Account (not found):"
curl -s $API_URL/api/v1/accounts/ACC99999999/verify | jq
echo ""

echo "4. Get Account Details:"
curl -s $API_URL/api/v1/accounts/ACC12345678 | jq
echo ""

echo "5. List All Customers:"
curl -s $API_URL/api/v1/customers | jq '.count'
echo ""

echo "6. Search Customers:"
curl -s "$API_URL/api/v1/customers/search?q=john" | jq
```

Save as `test_api.sh` and run:
```bash
chmod +x test_api.sh
./test_api.sh
```

## Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY flask_api.py .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "flask_api:app"]
```

Build and run:
```bash
docker build -t mock-crm-api .
docker run -p 8080:8080 mock-crm-api
```

## Security Notes

⚠️ **This is a demo/mock API only!**

- No authentication required (for demo purposes)
- Data is stored in memory (resets on restart)
- Not suitable for production use
- Use only for testing and demonstrations

For production, you would need:
- Authentication (API keys, OAuth)
- Database persistence
- Rate limiting
- HTTPS/TLS
- Input validation
- Logging and monitoring

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### Dependencies Not Installing
```bash
# Use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### CORS Issues
The API has CORS enabled for all origins. If you still have issues:
- Check browser console for errors
- Verify the API URL is correct
- Try using the API from curl first

## Files

- `customer-database.json` - Customer data in JSON format
- `crm_api.py` - IBM Cloud Functions version
- `flask_api.py` - Flask REST API (recommended)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Support

For issues or questions about the mock CRM API, check:
- API is running: `curl http://localhost:8080/health`
- Logs: Check terminal output where API is running
- Test with curl before integrating with Orchestrate

---

**Quick Start for Demo:**
```bash
cd mock-crm
pip install -r requirements.txt
python flask_api.py
# API now running at http://localhost:8080