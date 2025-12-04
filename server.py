import os
from fastapi import FastAPI, UploadFile, File, Response, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from facebook.csv_handler import process_csv
from facebook.router import router as facebook_router
from facebook.auth import get_access_token, get_login_url
from dotenv import load_dotenv

load_dotenv()  # load .env

AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")  # Get from .env

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(facebook_router, prefix="/facebook", tags=["Facebook"])

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Home
@app.get("/")
def home():
    return {
        "message": "Meta CSV Uploader Running",
        "ad_account_id": AD_ACCOUNT_ID
    }

# Facebook login POST endpoint
@app.post("/facebook/login")
def facebook_login():
    """Return Facebook login URL for frontend to redirect"""
    login_url = get_login_url()
    return {"login_url": login_url}

# CSV Upload Form
@app.get("/upload-campaign-csv")
def upload_campaign_csv_form():
    return HTMLResponse(f"""
    <html>
    <head>
        <title>Upload Campaign CSV</title>
        <style>
            body {{ font-family: Arial; background: #f0f2f5; display: flex; justify-content: center; padding-top: 50px; }}
            .box {{ background: white; padding: 20px; border-radius: 8px; width: 350px; text-align: center; }}
            .login-link {{ color: #1877f2; text-decoration: none; margin-bottom: 20px; display: block; }}
            .login-link:hover {{ text-decoration: underline; }}
            button {{ padding: 8px 14px; background: #1877f2; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Upload Campaign CSV</h2>
            <a href="/facebook/auth/login" class="login-link" target="_blank">Login with Facebook First</a>
            <form action="/upload-campaign-csv" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".csv" required />
                <br><br>
                <button type="submit">Upload & Create</button>
            </form>
        </div>
    </body>
    </html>
    """)

# Process CSV & Create Ads
@app.post("/upload-campaign-csv")
async def upload_campaign_csv(file: UploadFile = File(...)):
    access_token = get_access_token()
    if not access_token:
        return {"error": "Please login via Facebook first: /facebook/login"}

    if not file.filename.endswith(".csv"):
        return {"error": "Upload only CSV files"}

    try:
        # Only pass the file; access token is obtained inside process_csv
        results = await process_csv(file)
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
