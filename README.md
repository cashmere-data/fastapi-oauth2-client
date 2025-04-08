# FastAPI OAuth 2.0 Client for Cashmere Publishing

This repository provides a simple yet complete example of implementing OAuth 2.0 integration with **Cashmere Publishing**, using the FastAPI framework and the PKCE (Proof Key for Code Exchange) flow. It allows you to quickly test and develop an OAuth 2.0 authorization flow, enabling your application to securely access resources protected by Cashmere Publishing's OAuth 2.0 provider.

---

## Overview

This project demonstrates a typical OAuth 2.0 Authorization Code flow using:

- **FastAPI** as the web framework.
- **PKCE (Proof Key for Code Exchange)** to enhance security without relying on client secrets stored on the client side.
- **Uvicorn** for local development and testing.
- **Ngrok** for exposing your local server securely to the public internet (useful for OAuth callbacks).

The application consists of two main endpoints:

- `/login`: Initiates the OAuth 2.0 authorization flow.
- `/callback`: Handles the redirect from Cashmere Publishing, exchanges the authorization code for tokens, and returns the token information.

---

## Prerequisites

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Requests](https://docs.python-requests.org/en/master/)
- [Ngrok](https://ngrok.com/) (recommended for development/testing)

---

## Installation

Clone this repository:

```bash
git clone <your-repo-url>
cd fastapi-oauth2-client
```

Install dependencies (ideally in a virtual environment):

```bash
pip install fastapi uvicorn requests
```

---

## Configuration

Edit the configuration variables in `main.py`:

```python
# main.py

BASE_URL = "https://your-ngrok-url.ngrok.app" # Replace with your ngrok or deployed URL
DJANGO_BASE_URL = "https://omnibk.ai" # Cashmere Publishing OAuth provider URL

CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret" # Usually needed for token exchange
REDIRECT_URI = f"{BASE_URL}/callback"
SCOPE = "read write" # Adjust scopes as provided by Cashmere Publishing
```

**Note:**  
You will need to obtain your OAuth credentials (`CLIENT_ID` and `CLIENT_SECRET`) from Cashmere Publishing's OAuth dashboard or administrator.

---

## Running the App

Start the server using Uvicorn:

```bash
uvicorn main:app --host localhost --port 3000
```

### Exposing your server with Ngrok (Recommended)

Since OAuth callbacks require a public URL, you can use ngrok to expose your local FastAPI server:

```bash
ngrok http 3000
```

Once running, replace `BASE_URL` in `main.py` with the generated ngrok URL, e.g.:

```python
BASE_URL = "https://f299b727be99.ngrok.app"
```

---

## Usage

### Step 1: Begin OAuth Flow

Navigate to:

```
http://localhost:3000/login
```

This will redirect you to Cashmere Publishing's OAuth authorization page.

### Step 2: Authorize Application

Log in (if needed) and authorize the application.

### Step 3: Callback & Tokens

After authorization, you'll be redirected back to your callback endpoint. The tokens (`access_token`, `refresh_token`, etc.) from Cashmere Publishing will be displayed as a JSON response:

```json
{
  "access_token": "your-access-token",
  "refresh_token": "your-refresh-token",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "read write"
}
```

---

## Notes for Production

- Store sensitive information (`CLIENT_SECRET`, tokens, etc.) securely, ideally in environment variables or a secure credential manager.
- Replace the in-memory `oauth_store` with a secure session storage solution.

---

## License

MIT License

---

## Support

For additional help integrating with Cashmere Publishing, contact their technical support or consult the official OAuth documentation provided by Cashmere Publishing.
