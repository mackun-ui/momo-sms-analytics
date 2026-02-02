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