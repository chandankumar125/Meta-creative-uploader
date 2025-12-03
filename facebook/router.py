from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from .auth import get_login_url, exchange_code_for_token, get_long_lived_token, set_access_token

router = APIRouter()

@router.get("/auth/login")
def login():
    """Redirects the user to the Facebook Login Dialog."""
    login_url = get_login_url()
    return RedirectResponse(url=login_url)

@router.get("/auth/callback")
def callback(code: str):
    """Handles the callback from Facebook, exchanges code for token."""
    try:
        # Exchange code for short-lived token
        token_data = exchange_code_for_token(code)
        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error"]["message"])
        
        short_lived_token = token_data.get("access_token")
        
        # Exchange for long-lived token
        long_lived_data = get_long_lived_token(short_lived_token)
        if "error" in long_lived_data:
             raise HTTPException(status_code=400, detail=long_lived_data["error"]["message"])

        long_lived_token = long_lived_data.get("access_token")

        # Store the token globally for use in other modules
        set_access_token(long_lived_token)

        return {
            "message": "Login successful. Token stored.",
            "short_lived_token": short_lived_token,
            "long_lived_token": long_lived_token
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
