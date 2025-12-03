import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
API_VERSION = "v18.0"

# Global storage for the access token (Simple solution for local single-user tool)
_ACCESS_TOKEN = None

def set_access_token(token):
    global _ACCESS_TOKEN
    _ACCESS_TOKEN = token

def get_access_token():
    return _ACCESS_TOKEN

def get_login_url():
    """Generates the Facebook Login URL."""
    return (
        f"https://www.facebook.com/{API_VERSION}/dialog/oauth?"
        f"client_id={APP_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=ads_management,ads_read,business_management"
    )

def exchange_code_for_token(code: str):
    """Exchanges the authorization code for a short-lived access token."""
    url = (
        f"https://graph.facebook.com/{API_VERSION}/oauth/access_token?"
        f"client_id={APP_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"client_secret={APP_SECRET}&"
        f"code={code}"
    )
    response = requests.get(url)
    return response.json()

def get_long_lived_token(short_lived_token: str):
    """Exchanges a short-lived token for a long-lived token."""
    url = (
        f"https://graph.facebook.com/{API_VERSION}/oauth/access_token?"
        f"grant_type=fb_exchange_token&"
        f"client_id={APP_ID}&"
        f"client_secret={APP_SECRET}&"
        f"fb_exchange_token={short_lived_token}"
    )
    response = requests.get(url)
    return response.json()
