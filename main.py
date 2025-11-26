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
    
    return {"success": True, "video_creative_id": creative_id, **data}

# -------------------------------
# Upload Thumbnail
# -------------------------------
@app.post("/upload-thumbnail")
async def upload_thumbnail(video_id: str, file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No thumbnail uploaded")

    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    url = f"https://graph.facebook.com/v24.0/{video_id}/thumbnails"
    
    with open(temp_path, "rb") as f:
        response = requests.post(
            url,
            files={"source": f},
            data={"access_token": ACCESS_TOKEN}
        )

    os.remove(temp_path)
    data = response.json()
    
    thumbnail_id = data.get("id", None)
    
    return {"success": True, "thumbnail_id": thumbnail_id, **data}

# -------------------------------
# Home route
# -------------------------------
@app.get("/")
def home():
    return {"message": "Meta Upload API Working!"}
