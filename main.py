# main.py

import secrets
import hashlib
import base64
import urllib.parse

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import requests

PORT=3000
HOST="localhost"
DOMAIN=f"http://{HOST}"
# BASE_URL=f"{DOMAIN}:{PORT}"
BASE_URL="https://f299b727be99.ngrok.app" # Replace with your ngrok URL
DJANGO_BASE_URL="https://omnibk.ai"


app = FastAPI()

# Configuration (adjust these as needed)
CLIENT_ID = "qan9LTAgHxCzClAOSV1oJFCGl9FygFXsjA0bZtxF" # Replace with your client ID
CLIENT_SECRET = "HYn8ew4vHNf8yRl7En9mLECRMBjAvHBVkRXluOmuocU3xqyC26wGetI7ML47euuhnGf8Emr7cKqHxrcsbYmEvq1ZUd0n5Mh9SPzU00xn3E1uGfl2x2zC48nUowU37tu0" # Replace with your client secret (if needed for token exchange)
REDIRECT_URI = f"{BASE_URL}/callback" 
SCOPE = "read write"                   # Adjust scopes as required
DJANGO_AUTHORIZE_URL = f"{DJANGO_BASE_URL}/o/authorize/"
DJANGO_TOKEN_URL = f"{DJANGO_BASE_URL}/o/token/"

# For simplicity, we store the code_verifier and state in a dict.
# In production, use a secure, per-user session store.
oauth_store = {}

def base64url_encode(input_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(input_bytes).decode('utf-8').rstrip('=')

def generate_pkce_pair() -> tuple[str, str]:
    # Generate a secure code_verifier
    code_verifier = base64url_encode(secrets.token_bytes(32))
    # Create the code_challenge: SHA256 hash then base64url encode
    code_challenge = base64url_encode(hashlib.sha256(code_verifier.encode('utf-8')).digest())
    return code_verifier, code_challenge

@app.get("/login")
def login():
    # Generate a random state and PKCE pair
    state = secrets.token_urlsafe(16)
    code_verifier, code_challenge = generate_pkce_pair()

    # Save the code_verifier associated with this state (for later validation)
    oauth_store[state] = code_verifier

    # Build the authorization URL with query parameters
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    url = f"{DJANGO_AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@app.get("/callback")
def callback(request: Request, code: str = None, state: str = None, error: str = None):
    print("Received state:", state)
    print("Available states:", list(oauth_store.keys()))
    # Check for errors in the query parameters
    if error:
        raise HTTPException(status_code=400, detail=f"Error returned: {error}")
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state in callback")

    # Retrieve the original code_verifier
    code_verifier = oauth_store.get(state)
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Invalid or expired state parameter")

    # Prepare the token request payload
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier,
    }

    # If your token endpoint requires HTTP Basic Auth, set it up:
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    basic_auth = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Exchange the authorization code for tokens
    token_response = requests.post(DJANGO_TOKEN_URL, data=data, headers=headers)
    if token_response.status_code != 200:
        raise HTTPException(status_code=token_response.status_code,
                            detail=f"Token request failed: {token_response.text}")

    # Optionally remove the used state and code_verifier
    # oauth_store.pop(state, None)
    print(f"Token response: {token_response.json()}\nOauth store: {oauth_store}")

    # Return the token response as JSON
    return JSONResponse(token_response.json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)