"""
Test script for REST API endpoints
Run this after starting the API server: python api/app.py
"""

import requests
import json
import base64

BASE_URL = "http://localhost:8000"

# Create auth header
credentials = "admin:password123"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
auth_header = f"Basic {encoded_credentials}"

headers = {
    "Authorization": auth_header,
    "Content-Type": "application/json"
}

print("=" * 60)
print("🧪 Testing MoMo SMS Transaction API")
print("=" * 60)

# Test 1: GET all transactions
print("\n1️⃣  TEST: GET /transactions (with auth)")
try:
    response = requests.get(f"{BASE_URL}/transactions", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success! Found {data['count']} transactions")
        print(f"   First transaction: ID={data['transactions'][0]['id']}, Type={data['transactions'][0]['type']}")
    else:
        print(f"   ❌ Error: {response.json()}")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")

# Test 2: GET single transaction
print("\n2️⃣  TEST: GET /transactions/1 (with auth)")
try:
    response = requests.get(f"{BASE_URL}/transactions/1", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success!")
        print(f"   Transaction: {json.dumps(data, indent=6)[:200]}...")
    else:
        print(f"   ❌ Error: {response.json()}")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")

# Test 3: Unauthorized request
print("\n3️⃣  TEST: GET /transactions (NO auth)")
try:
    response = requests.get(f"{BASE_URL}/transactions")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print(f"   ✅ Correctly rejected! {response.json()}")
    else:
        print(f"   ❌ Should have been 401: {response.json()}")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")

# Test 4: POST new transaction
print("\n4️⃣  TEST: POST /transactions (create)")
new_transaction = {
    "type": "SENT",
    "amount": 15000,
    "receiver": "Test User",
    "sender": "You",
    "fee": 100,
    "balance": 50000
}
try:
    response = requests.post(f"{BASE_URL}/transactions", headers=headers, json=new_transaction)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"   ✅ Created! New ID: {data['id']}")
        created_id = data['id']
    else:
        print(f"   ❌ Error: {response.json()}")
        created_id = None
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    created_id = None

# Test 5: PUT update transaction
if created_id:
    print(f"\n5️⃣  TEST: PUT /transactions/{created_id} (update)")
    updates = {
        "amount": 20000,
        "receiver": "Updated User"
    }
    try:
        response = requests.put(f"{BASE_URL}/transactions/{created_id}", headers=headers, json=updates)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Updated! New amount: {data['amount']}, Receiver: {data['receiver']}")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")

# Test 6: DELETE transaction
if created_id:
    print(f"\n6️⃣  TEST: DELETE /transactions/{created_id}")
    try:
        response = requests.delete(f"{BASE_URL}/transactions/{created_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 204:
            print(f"   ✅ Deleted successfully!")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")

# Test 7: Verify deletion
if created_id:
    print(f"\n7️⃣  TEST: GET /transactions/{created_id} (verify deletion)")
    try:
        response = requests.get(f"{BASE_URL}/transactions/{created_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly returns 404!")
        else:
            print(f"   ❌ Should be 404: {response.json()}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")

print("\n" + "=" * 60)
print("✅ All tests complete!")
print("=" * 60)
