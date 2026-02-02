
import requests
import json
import base64
from datetime import datetime


class APITester:
    """Test suite for Transaction API"""
    
    def __init__(self, base_url='http://localhost:8000', username='admin', password='password'):
        """
        Initialize API tester.
        
        Args:
            base_url: Base URL of the API
            username: Username for Basic Auth
            password: Password for Basic Auth
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        
    def _get_auth_header(self, username=None, password=None):
        """
        Generate Basic Auth header.
        
        Args:
            username: Username (uses default if None)
            password: Password (uses default if None)
            
        Returns:
            dict: Headers with Authorization
        """
        user = username or self.username
        pwd = password or self.password
        
        # Encode credentials
        credentials = f"{user}:{pwd}"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        return {
            'Authorization': f'Basic {encoded}',
            'Content-Type': 'application/json'
        }
    
    def test_get_all_transactions(self):
        """Test GET /transactions endpoint"""
        print("\n" + "="*60)
        print("TEST 1: GET /transactions (List all transactions)")
        print("="*60)
        
        url = f"{self.base_url}/transactions"
        headers = self._get_auth_header()
        
        try:
            response = self.session.get(url, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Number of transactions: {len(data)}")
                print(f"Sample transaction: {json.dumps(data[0] if data else {}, indent=2)}")
                print("✓ TEST PASSED")
            else:
                print(f"Response: {response.text}")
                print("✗ TEST FAILED")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    def test_get_single_transaction(self, transaction_id=1):
        """Test GET /transactions/{id} endpoint"""
        print("\n" + "="*60)
        print(f"TEST 2: GET /transactions/{transaction_id} (Get single transaction)")
        print("="*60)
        
        url = f"{self.base_url}/transactions/{transaction_id}"
        headers = self._get_auth_header()
        
        try:
            response = self.session.get(url, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Transaction found: {json.dumps(data, indent=2)}")
                print("✓ TEST PASSED")
            elif response.status_code == 404:
                print(f"Transaction not found (404)")
                print("✓ TEST PASSED (404 is expected for non-existent ID)")
            else:
                print(f"Response: {response.text}")
                print("✗ TEST FAILED")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    def test_post_transaction(self):
        """Test POST /transactions endpoint"""
        print("\n" + "="*60)
        print("TEST 3: POST /transactions (Create new transaction)")
        print("="*60)
        
        url = f"{self.base_url}/transactions"
        headers = self._get_auth_header()
        
        # Sample transaction data
        new_transaction = {
            "type": "send",
            "amount": 50000.00,
            "sender": "0788123456",
            "receiver": "0788654321",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "message": "Payment for services"
        }
        
        print(f"Sending data: {json.dumps(new_transaction, indent=2)}")
        
        try:
            response = self.session.post(url, headers=headers, json=new_transaction)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                print(f"Created transaction: {json.dumps(data, indent=2)}")
                print("✓ TEST PASSED")
                return data.get('id')  # Return ID for later tests
            else:
                print(f"Response: {response.text}")
                print("✗ TEST FAILED")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
        
        return None
    
    def test_put_transaction(self, transaction_id=1):
        """Test PUT /transactions/{id} endpoint"""
        print("\n" + "="*60)
        print(f"TEST 4: PUT /transactions/{transaction_id} (Update transaction)")
        print("="*60)
        
        url = f"{self.base_url}/transactions/{transaction_id}"
        headers = self._get_auth_header()
        
        # Updated data
        updated_data = {
            "amount": 75000.00,
            "message": "Updated payment amount"
        }
        
        print(f"Sending update: {json.dumps(updated_data, indent=2)}")
        
        try:
            response = self.session.put(url, headers=headers, json=updated_data)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Updated transaction: {json.dumps(data, indent=2)}")
                print("✓ TEST PASSED")
            elif response.status_code == 404:
                print(f"Transaction not found (404)")
                print("✓ TEST PASSED (404 is expected for non-existent ID)")
            else:
                print(f"Response: {response.text}")
                print("✗ TEST FAILED")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    def test_delete_transaction(self, transaction_id):
        """Test DELETE /transactions/{id} endpoint"""
        print("\n" + "="*60)
        print(f"TEST 5: DELETE /transactions/{transaction_id} (Delete transaction)")
        print("="*60)
        
        url = f"{self.base_url}/transactions/{transaction_id}"
        headers = self._get_auth_header()
        
        try:
            response = self.session.delete(url, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"Transaction deleted successfully")
                print("✓ TEST PASSED")
            elif response.status_code == 404:
                print(f"Transaction not found (404)")
                print("✓ TEST PASSED (404 is expected for non-existent ID)")
            else:
                print(f"Response: {response.text}")
                print("✗ TEST FAILED")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    def test_unauthorized_access(self):
        """Test authentication failure with wrong credentials"""
        print("\n" + "="*60)
        print("TEST 6: Unauthorized Access (Wrong credentials)")
        print("="*60)
        
        url = f"{self.base_url}/transactions"
        # Use wrong credentials
        headers = self._get_auth_header(username='wrong', password='wrongpass')
        
        try:
            response = self.session.get(url, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 401:
                print(f"Response: {response.text}")
                print("✓ TEST PASSED (401 Unauthorized)")
            else:
                print(f"Response: {response.text}")
                print("✗ TEST FAILED (Should return 401)")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    def test_no_authentication(self):
        """Test request without authentication header"""
        print("\n" + "="*60)
        print("TEST 7: No Authentication Header")
        print("="*60)
        
        url = f"{self.base_url}/transactions"
        # No authentication header
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = self.session.get(url, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 401:
                print(f"Response: {response.text}")
                print("✓ TEST PASSED (401 Unauthorized)")
            else:
                print(f"Response: {response.text}")
                print("✗ TEST FAILED (Should return 401)")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("\n" + "#"*60)
        print("# TRANSACTION API TEST SUITE")
        print("#"*60)
        print(f"Base URL: {self.base_url}")
        print(f"Username: {self.username}")
        print(f"Testing started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test authentication failures first
        self.test_unauthorized_access()
        self.test_no_authentication()
        
        # Test successful operations
        self.test_get_all_transactions()
        self.test_get_single_transaction(1)
        
        # Create a new transaction and use its ID for update/delete
        new_id = self.test_post_transaction()
        
        if new_id:
            self.test_put_transaction(new_id)
            self.test_delete_transaction(new_id)
        else:
            # Fallback to testing with ID 1
            self.test_put_transaction(1)
            self.test_delete_transaction(1)
        
        print("\n" + "#"*60)
        print("# ALL TESTS COMPLETED")
        print("#"*60)
        print(f"Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def generate_curl_commands():
    """Generate curl commands for manual testing"""
    print("\n" + "="*60)
    print("CURL COMMANDS FOR MANUAL TESTING")
    print("="*60)
    
    base64_creds = base64.b64encode(b'admin:password').decode()
    
    commands = {
        "GET all transactions": f'''curl -X GET http://localhost:8000/transactions \\
  -H "Authorization: Basic {base64_creds}"''',
        
        "GET single transaction": f'''curl -X GET http://localhost:8000/transactions/1 \\
  -H "Authorization: Basic {base64_creds}"''',
        
        "POST new transaction": f'''curl -X POST http://localhost:8000/transactions \\
  -H "Authorization: Basic {base64_creds}" \\
  -H "Content-Type: application/json" \\
  -d '{{"type":"send","amount":50000,"sender":"0788123456","receiver":"0788654321"}}'
''',
        
        "PUT update transaction": f'''curl -X PUT http://localhost:8000/transactions/1 \\
  -H "Authorization: Basic {base64_creds}" \\
  -H "Content-Type: application/json" \\
  -d '{{"amount":75000}}'
''',
        
        "DELETE transaction": f'''curl -X DELETE http://localhost:8000/transactions/1 \\
  -H "Authorization: Basic {base64_creds}"''',
        
        "Test unauthorized (wrong password)": '''curl -X GET http://localhost:8000/transactions \\
  -H "Authorization: Basic d3Jvbmc6d3Jvbmc="'''
    }
    
    for name, command in commands.items():
        print(f"\n{name}:")
        print("-" * 40)
        print(command)


if __name__ == '__main__':
    # Initialize tester
    tester = APITester(
        base_url='http://localhost:8000',
        username='admin',
        password='password'
    )
    
    print("""
╔════════════════════════════════════════════════════════════╗
║          TRANSACTION API TESTING SCRIPT                    ║
║          Member C - Backend Support                        ║
╚════════════════════════════════════════════════════════════╝

This script will test all API endpoints with authentication.

PREREQUISITES:
1. Make sure the API server is running (python api/app.py)
2. The API should be accessible at http://localhost:8000
3. Default credentials: admin / password

""")
    
    try:
        # Run all tests
        tester.run_all_tests()
        
        # Generate curl commands
        generate_curl_commands()
        
        print("\n\n✓ Testing script completed successfully!")
        print("\nNOTE: Save screenshots of these test results for your assignment.")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to API server!")
        print("\nPlease ensure:")
        print("1. The API server is running (python api/app.py)")
        print("2. The API is listening on http://localhost:8000")
        print("\nStart the server first, then run this script again.")
    
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user.")
    
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
