import csv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import requests
from typing import Optional
app = FastAPI(title="Meta Upload API", version="1.0")

ACCESS_TOKEN="EAAQeYqt2zH4BQMNm9RRLNJAuAfnqQ72wfdNFJ2WxbL9XhPlHeBVo41OjpTvkZAEIN0ySZCyHf3lC2f1YiQJ32itKRQXq6Yz2xt5RNsKk2RXryCEGxhSbAaUgLaLwKrVL7uu11scZBnSRWoLvqPkwZBePpDhz2xzMUjUads91cEH6bYZBwkO5ZBqtDavfL0nZARjSz3z"
AD_ACCOUNT_ID="1324697116076599"

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

CSV_FILE = "meta_upload_log.csv"

# Initialize CSV file with header if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file_type", "image_hash", "video_id", "thumbnail_id", "creative_id"])

# -------------------------------
# Helper to save row to CSV
# -------------------------------
def save_to_csv(file_type, image_hash=None, video_id=None, thumbnail_id=None, creative_id=None):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([file_type, image_hash, video_id, thumbnail_id, creative_id])

# -------------------------------
# Upload Image
# -------------------------------
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    url = f"https://graph.facebook.com/v24.0/act_{AD_ACCOUNT_ID}/adimages"
    
    with open(temp_path, "rb") as f:
        response = requests.post(
            url,
            files={"file": f},
            data={"access_token": ACCESS_TOKEN}
        )

    os.remove(temp_path)
    data = response.json()
    
    if "images" in data:
        image_hash = list(data["images"].values())[0]["hash"]
        save_to_csv("image", image_hash=image_hash)
        return {"success": True, "image_hash": image_hash}
    
    return JSONResponse(status_code=response.status_code, content=data)

# -------------------------------
# Upload Video
# -------------------------------
@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...), title: Optional[str] = "Uploaded via FastAPI"):
    if not file:
        raise HTTPException(status_code=400, detail="No video uploaded")
    
    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    url = f"https://graph.facebook.com/v24.0/act_{AD_ACCOUNT_ID}/advideos"
    
    with open(temp_path, "rb") as f:
        response = requests.post(
            url,
            files={"file": f},
            data={
                "access_token": ACCESS_TOKEN,
                "title": title
            }
        )

    os.remove(temp_path)
    data = response.json()
    
    creative_id = data.get("id", None)
    save_to_csv("video", creative_id=creative_id)
    
    return {"success": True, "video_creative_id": creative_id, **data}

# -------------------------------
# Get Video Thumbnails
# -------------------------------
@app.get("/video-thumbnails")
async def get_video_thumbnails(video_id: str):
    """
    Retrieve thumbnails of a video from Facebook Graph API.
    """
    if not video_id:
        raise HTTPException(status_code=400, detail="video_id is required")

    url = f"https://graph.facebook.com/v24.0/{video_id}/thumbnails"
    
    response = requests.get(
        url,
        params={"access_token": ACCESS_TOKEN}
    )

    data = response.json()
    
    if "error" in data:
        return {"success": False, "error": data["error"]}

    thumbnails = []
    for item in data.get("data", []):
        thumbnails.append({
            "id": item.get("id"),
            "uri": item.get("uri"),
            "height": item.get("height"),
            "width": item.get("width"),
            "scale": item.get("scale"),
            "is_preferred": item.get("is_preferred")
        })
        # Save each thumbnail row in CSV
        save_to_csv("thumbnail", video_id=video_id, thumbnail_id=item.get("id"))

    return {"success": True, "video_id": video_id, "thumbnails": thumbnails}

# -------------------------------
# Home route
# -------------------------------
@app.get("/")
def home():
    return {"message": "Meta Upload API Working!"}
