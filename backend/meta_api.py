import requests
from config import ACCESS_TOKEN, AD_ACCOUNT_ID

def upload_image(image_path):
    """Upload image to Meta API."""
    try:
        with open(image_path, "rb") as f:
            res = requests.post(
                f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/adimages",
                files={"filename": f},
                data={"access_token": ACCESS_TOKEN}
            )
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def upload_video(video_path):
    """Upload video to Meta API."""
    try:
        with open(video_path, "rb") as f:
            res = requests.post(
                f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/advideos",
                files={"file": f},
                data={"access_token": ACCESS_TOKEN}
            )
        return res.json()
    except Exception as e:
        return {"error": str(e)}
