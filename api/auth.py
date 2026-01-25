"""
Basic Authentication Module

Implements HTTP Basic Authentication for the REST API.
WARNING: Basic Auth is NOT secure without HTTPS!
"""

import base64
from typing import Optional, Tuple


# Hardcoded credentials for assignment (NOT production-ready!)
VALID_CREDENTIALS = {
    "admin": "password123",
    "user": "user123"
}


def parse_auth_header(auth_header: Optional[str]) -> Optional[Tuple[str, str]]:
    """
    Parse Basic Authentication header
    
    Args:
        auth_header: Authorization header value (e.g., "Basic base64string")
        
    Returns:
        Tuple of (username, password) if valid format, None otherwise
    """
    if not auth_header:
        return None
    
    try:
        # Expected format: "Basic <base64_encoded_credentials>"
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0] != 'Basic':
            return None
        
        # Decode base64 credentials
        credentials = base64.b64decode(parts[1]).decode('utf-8')
        
        # Split username:password
        if ':' not in credentials:
            return None
        
        username, password = credentials.split(':', 1)
        return (username, password)
    
    except (ValueError, UnicodeDecodeError):
        return None


def verify_credentials(username: str, password: str) -> bool:
    """
    Verify username and password against valid credentials
    
    Args:
        username: Username to verify
        password: Password to verify
        
    Returns:
        True if credentials are valid, False otherwise
    """
    return VALID_CREDENTIALS.get(username) == password


def check_authentication(auth_header: Optional[str]) -> bool:
    """
    Check if the Authorization header contains valid credentials
    
    Args:
        auth_header: Authorization header value
        
    Returns:
        True if authenticated, False otherwise
    """
    credentials = parse_auth_header(auth_header)
    
    if not credentials:
        return False
    
    username, password = credentials
    return verify_credentials(username, password)
