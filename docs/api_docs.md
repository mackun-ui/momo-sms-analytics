# MoMo SMS Transactions API Documentation

## Authentication
All endpoints require Basic Authentication.
- Username: 'admin'
- Password: 'momosmsanalysis'

Unauthorised requests return **401 Unauthorized**

Header Example:
```http
Authorization: Basic YWRtaW46bW9tb3Ntc2FkanFz
```
## Endpoints

### 1. GET /transactions - List all transactions
- Description: Retrieves a list of all SMS transactions.
- Request Example:  
```http
GET /transaction HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46bW9tb3Ntc2FkanFz
```
- Response Example (200 OK):
```json
[
    {
        "id": 1,
        "sender": "Ama Mensah",
        "receiver": "Berima Kofi",
        "amount": 100,
        "type": "credit",
        "timestamp": "2026-02-01T10:00:00"
    }
]
```
- Error Codes: 
    - 401 Unauthorized - Missing or wrong credentials

### 2. GET /transactions/{id} - Retrieve a single transaction
- Description: Get details of one transaction by ID
- Request Example: 
```http
GET /transactions/1 HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46bW9tb3Ntc2FkanFz
```

- Response Example (200 OK):
```json
{
    "id": 1,
    "sender": "Ama Mensah",
    "receiver": "Berima Kofi",
    "amount": 100,
    "type": "credit",
    "timestamp": "2026-02-01T10:00:00"
}
```

- Error Codes:
    - 401 Unauthorized - Invalid credentials 
    - 404 Not Found - Transaction ID does not exist
    - 400 Bad Request - Invalid ID format

### 3. POST /transactions - Add a new transaction
- Description: Create a SMS transaction.
- Request Example:
```http
POST /transactions HTTP/1.1
Host: Localhost:8000
Authorization Basic YWRtaW46bW9tb3Ntc2FkanFz
Content-Type: application/json

{
    "sender": "David",
    "receiver": "Nicole",
    "amount": 50,
    "type": "debit",
    "timestamp": 2026-02-01T11:00:00
}
```
- Response Example (201 Created):
```json
{
    "id": 2,
    "sender": "David",
    "receiver": "Nicole",
    "amount": 50,
    "type": "debit",
    "timestamp": "2026-02-01T11:00:00"
}
```
- Error Codes: 
    - 401 Unauthorized - Invalid Credentials
    - 400 Bad Request - Missing required fields or invald JSON

### 4. PUT /transactions/{id} - Update an existing transaction
- Description: Update fields of a transactions by ID.
- Request Example: 
```http
PUT /transactions/1 HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46bW9tb3Ntc2FkanFz
Content-Type: application/json

{
    "amount": 120
}
```
- Response Example (200 OK):
```json
{
    "id": 1,
    "sender": "Ama Mensah",
    "receiver": "Berima Kofi",
    "amount": 120,
    "type": "credit",
    "timestamp": "2026-02-01T10:00:00"
}
```
- Error Codes: 
    - 401 Unauthorized - Invalid credentials
    - 404 Not Found - Transaction ID does not exist
    - 400 Bad Request - Invalid JSON

### 5. DELETE /transactions/{id} - Delete a transaction
- Description: Remove a transaction by ID.
- Request Example:
```http
DELETE /transactions/1 HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46bW9tb3Ntc2FkanFz
```
- Response Example (200 OK):
```json
{
    "message": "Transaction deleted"
}
```
- Error Codes:
    - 401 Unauthorized - Invalid credentials
    - 404 Not Found - Transaction ID does not exist

### Notes
- All timestamps are in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
- For examples with screenshots, see the screenshots/ folder.
- Always use Basic Authentication - requests without it will fail.