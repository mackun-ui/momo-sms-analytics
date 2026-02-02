import base64

USERNAME = "admin"
PASSWORD = "momosmsanalysis"

def is_authenticated(headers):
    auth_header = headers.get("Authorisation")

    if not auth_header or not auth_header.startswith("Basic "):
        return False
    
    encoded_credentials = auth_header.split(" ")[1]
    decoded = base64.b64decode(encoded_credentials).decode("utf-8")
    username, password = decoded.split(":")

    return username == USERNAME and password == PASSWORD