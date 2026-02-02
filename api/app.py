from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from api.auth import is_authenticated

HOST = "localhost"
PORT = 8000

# temp in-memory storage (will later be replaced)
transactions = []

class TransactionHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, data=None):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode())
        
    def _unauthorised(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate",'Basic realm="Secure Area"')
        self.end_headers()

    def _check_auth(self):
        if not is_authenticated(self.headers):
            self._unauthorised()
            return False
        return True
    
    def do_GET(self):
        if not self._check_auth():
            return
        
        if self.path == "/transactions":
            self._send_response(200, transactions)
        elif self.path.startswith("/transactions/"):
            try:
                transaction_ID = int(self.path.split("/")[-1])
                transaction = next(
                    (t for t in transaction if t["id"] == transaction_ID),
                    None
                )

                if transaction:
                    self._send_response(200, transaction)
                else: 
                    self._send_response(404, {"error": "Transaction not found"})
            except ValueError:
                self._send_response(400, {"error" : "Invalid ID"})
    
    def do_POST(self):
        if not self._check_auth():
            return
        
        if self.path == "/transactions":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            new_transaction = json.load(body)

            new_transaction["id"] = len(transactions) + 1
            transactions.append(new_transaction)

            self._send_response(201, new_transaction)

    def do_PUT(self):
        if not self._check_auth():
            return
        
        if self.path.startswith("/transactions/"):
            transaction_ID = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            updated_data = json.loads(body)

            for transaction in transactions:
                if transaction["id"] == transaction_ID:
                    transaction.update(updated_data)
                    self._send_response(200, transaction)
                    return
            
            self._send_response(404, {"error": "Transaction not found"})
    
    def do_DELETE(self):
        if not self._check_auth():
            return
        
        if self.path.startswith("/transactions/"):
            transaction_ID = int(self.path.split("/")[-1])

            for transaction in transactions:
                if transaction["id"] == transaction_ID:
                    transactions.remove(transaction)
                    self._send_response(200, {"message": "Transaction deleted"})
                    return
            
            self._send_response(404, {"error": "Transaction not found"})