Root Directory

# server.py
Initialize FastAPI app.
Load environment variables.
Mount facebook router.
Facebook Module (facebook/)

# auth.py
get_login_url(): Construct Facebook Login Dialog URL.
exchange_code_for_token(code): Exchange authorization code for short-lived access token.
get_long_lived_token(short_token): Exchange short-lived token for long-lived token.
# router.py
GET /auth/login: Redirect user to Facebook Login.
GET /auth/callback: Handle Facebook redirect, exchange code, and store token.
# accounts.py
Placeholder/Basic implementation for fetching ad accounts (requires valid token).
# upload_media.py
Placeholder for media upload logic.
# csv_handler.py
Placeholder for CSV processing.

Manual Verification
Start Server: Run uvicorn server:app --reload.
Initiate Login: Navigate to http://localhost:8000/auth/login in a browser.
Authorize: Log in to Facebook and authorize the app.
Check Callback: Verify redirection to http://localhost:8000/auth/callback and successful token retrieval (check logs or response).
Verify Token: Use the retrieved token to fetch ad accounts (if      accounts.py is implemented).



python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload