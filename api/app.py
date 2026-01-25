"""
REST API Server for MoMo SMS Transactions
Built with plain Python http.server module (no frameworks)

Endpoints:
- GET    /transactions       - List all transactions
- GET    /transactions/{id}  - Get specific transaction
- POST   /transactions       - Create new transaction
- PUT    /transactions/{id}  - Update transaction
- DELETE /transactions/{id}  - Delete transaction

All endpoints require Basic Authentication.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.auth import check_authentication
from dsa.dictionary_lookup import create_transaction_dict, dict_lookup


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API"""
    
    # Class-level storage (in-memory database)
    transactions_dict: Dict[str, Dict[str, Any]] = {}
    next_id: int = 1
    
    @classmethod
    def load_transactions(cls, json_path: Path):
        """Load transactions from JSON file into memory"""
        with open(json_path, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
        
        # Create dictionary for O(1) lookups (DSA integration)
        cls.transactions_dict = create_transaction_dict(transactions)
        
        # Track next available ID
        if transactions:
            max_id = max(int(t['id']) for t in transactions)
            cls.next_id = max_id + 1
        
        print(f"✅ Loaded {len(transactions)} transactions into memory")
        print(f"🔑 Using dictionary lookup for O(1) access")
    
    def do_GET(self):
        """Handle GET requests"""
        # Check authentication first
        if not self._check_auth():
            return
        
        # Parse URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route to appropriate handler
        if path == '/transactions':
            self._get_all_transactions()
        elif path.startswith('/transactions/'):
            transaction_id = path.split('/')[-1]
            self._get_transaction_by_id(transaction_id)
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        if not self._check_auth():
            return
        
        if self.path == '/transactions':
            self._create_transaction()
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_PUT(self):
        """Handle PUT requests"""
        if not self._check_auth():
            return
        
        if self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            self._update_transaction(transaction_id)
        else:
            self._send_error(404, "Endpoint not found")
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self._check_auth():
            return
        
        if self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            self._delete_transaction(transaction_id)
        else:
            self._send_error(404, "Endpoint not found")
    
    def _check_auth(self) -> bool:
        """Verify authentication and send 401 if invalid"""
        auth_header = self.headers.get('Authorization')
        
        if not check_authentication(auth_header):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Transaction API"')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = {
                "error": "Unauthorized",
                "message": "Valid credentials required. Use Basic Authentication."
            }
            self.wfile.write(json.dumps(error_response).encode())
            return False
        
        return True
    
    def _get_all_transactions(self):
        """GET /transactions - Return all transactions"""
        transactions = list(self.transactions_dict.values())
        
        response = {
            "transactions": transactions,
            "count": len(transactions)
        }
        
        self._send_json(200, response)
    
    def _get_transaction_by_id(self, transaction_id: str):
        """GET /transactions/{id} - Return specific transaction using O(1) lookup"""
        # Using dictionary lookup (DSA integration)
        transaction = dict_lookup(self.transactions_dict, transaction_id)
        
        if transaction:
            self._send_json(200, transaction)
        else:
            self._send_error(404, f"Transaction with ID {transaction_id} not found")
    
    def _create_transaction(self):
        """POST /transactions - Create new transaction"""
        try:
            # Read and parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            if not body:
                self._send_error(400, "Request body is required")
                return
            
            new_transaction = json.loads(body)
            
            # Validate required fields
            required_fields = ['type', 'amount']
            missing_fields = [f for f in required_fields if f not in new_transaction]
            
            if missing_fields:
                self._send_error(400, f"Missing required fields: {', '.join(missing_fields)}")
                return
            
            # Generate new ID
            new_id = str(self.next_id)
            self.__class__.next_id += 1
            
            # Set default values
            transaction = {
                "id": new_id,
                "type": new_transaction.get('type', 'UNKNOWN'),
                "amount": float(new_transaction.get('amount', 0)),
                "fee": float(new_transaction.get('fee', 0)),
                "balance": float(new_transaction.get('balance', 0)),
                "sender": new_transaction.get('sender', ''),
                "receiver": new_transaction.get('receiver', ''),
                "timestamp": new_transaction.get('timestamp', ''),
                "readable_date": new_transaction.get('readable_date', ''),
                "transaction_id_external": new_transaction.get('transaction_id_external', ''),
                "body": new_transaction.get('body', '')
            }
            
            # Add to dictionary
            self.transactions_dict[new_id] = transaction
            
            # Return created transaction with 201 status
            self._send_json(201, transaction)
        
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON in request body")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def _update_transaction(self, transaction_id: str):
        """PUT /transactions/{id} - Update existing transaction"""
        try:
            # Check if transaction exists
            transaction = dict_lookup(self.transactions_dict, transaction_id)
            
            if not transaction:
                self._send_error(404, f"Transaction with ID {transaction_id} not found")
                return
            
            # Read and parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            if not body:
                self._send_error(400, "Request body is required")
                return
            
            updates = json.loads(body)
            
            # Update fields (preserve ID)
            for key, value in updates.items():
                if key != 'id':  # Don't allow ID changes
                    transaction[key] = value
            
            # Update in dictionary
            self.transactions_dict[transaction_id] = transaction
            
            # Return updated transaction
            self._send_json(200, transaction)
        
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON in request body")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def _delete_transaction(self, transaction_id: str):
        """DELETE /transactions/{id} - Delete transaction"""
        # Check if transaction exists
        transaction = dict_lookup(self.transactions_dict, transaction_id)
        
        if not transaction:
            self._send_error(404, f"Transaction with ID {transaction_id} not found")
            return
        
        # Delete from dictionary
        del self.transactions_dict[transaction_id]
        
        # Return 204 No Content
        self.send_response(204)
        self.end_headers()
    
    def _send_json(self, status_code: int, data: Any):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode())
    
    def _send_error(self, status_code: int, message: str):
        """Send error response"""
        error_response = {
            "error": self._get_status_message(status_code),
            "message": message
        }
        self._send_json(status_code, error_response)
    
    def _get_status_message(self, code: int) -> str:
        """Get status message for HTTP code"""
        messages = {
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error"
        }
        return messages.get(code, "Error")
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(host: str = 'localhost', port: int = 8000):
    """
    Start the REST API server
    
    Args:
        host: Server host
        port: Server port
    """
    # Load transactions from JSON file
    json_path = Path(__file__).parent.parent / "data" / "processed" / "transactions.json"
    
    if not json_path.exists():
        print("❌ transactions.json not found!")
        print("   Run: python etl/parse_xml.py first")
        return
    
    TransactionAPIHandler.load_transactions(json_path)
    
    # Start server
    server = HTTPServer((host, port), TransactionAPIHandler)
    
    print("\n" + "=" * 60)
    print("🚀 MoMo SMS Transaction API Server")
    print("=" * 60)
    print(f"📡 Server running at: http://{host}:{port}")
    print(f"🔐 Authentication: Basic Auth required")
    print(f"👤 Credentials: admin:password123")
    print(f"\n📚 Endpoints:")
    print(f"   GET    /transactions       - List all")
    print(f"   GET    /transactions/{{id}}  - Get one")
    print(f"   POST   /transactions       - Create new")
    print(f"   PUT    /transactions/{{id}}  - Update")
    print(f"   DELETE /transactions/{{id}}  - Delete")
    print("\n⌨️  Press Ctrl+C to stop server")
    print("=" * 60 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        server.shutdown()


if __name__ == "__main__":
    run_server()
