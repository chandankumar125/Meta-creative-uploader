from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = "EAAQeYqt2zH4BQMNm9RRLNJAuAfnqQ72wfdNFJ2WxbL9XhPlHeBVo41OjpTvkZAEIN0ySZCyHf3lC2f1YiQJ32itKRQXq6Yz2xt5RNsKk2RXryCEGxhSbAaUgLaLwKrVL7uu11scZBnSRWoLvqPkwZBePpDhz2xzMUjUads91cEH6bYZBwkO5ZBqtDavfL0nZARjSz3z"
AD_ACCOUNT_ID = "1324697116076599"


# -----------------------------
# 1. Upload IMAGE to Meta
# -----------------------------
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    url = f"https://graph.facebook.com/v19.0/act_{AD_ACCOUNT_ID}/adimages"

    with open(temp_path, 'rb') as f:
        response = requests.post(
            url,
            files={"file": f},
            data={"access_token": ACCESS_TOKEN}
        )

    os.remove(temp_path)

    raw = response.json()
    image_hash = ""

    # FIX: correctly extract image hash
    if "images" in raw:
        first_key = next(iter(raw["images"]))
        image_hash = raw["images"][first_key].get("hash", "")

    return jsonify({
        "file_type": "image",
        "image_hash": image_hash,
        "video_id": "",
        "thumbnail_id": "",
        "creative_id": ""
    })


# -----------------------------
# 2. Upload VIDEO to Meta
# -----------------------------
@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    file = request.files['file']
    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    # STEP 1 → Upload video
    upload_url = f"https://graph.facebook.com/v24.0/act_{AD_ACCOUNT_ID}/advideos"

    with open(temp_path, 'rb') as f:
        response = requests.post(
            upload_url,
            files={"file": f},
            data={
                "access_token": ACCESS_TOKEN,
                "title": "Uploaded via Flask"
            }
        )

    os.remove(temp_path)

    data = response.json()
    video_id = data.get("id", "")

    if not video_id:
        return jsonify({"error": "Video upload failed", "response": data}), 400

    # STEP 2 → Fetch thumbnail
    thumb_url = f"https://graph.facebook.com/v24.0/{video_id}/thumbnails"
    thumb_res = requests.get(
        thumb_url,
        params={"access_token": ACCESS_TOKEN}
    ).json()

    thumbnail_id = ""
    if "data" in thumb_res and len(thumb_res["data"]) > 0:
        thumbnail_id = thumb_res["data"][0].get("id", "")




    # STEP 3 → Create ad creative
    creative_url = f"https://graph.facebook.com/v19.0/act_{AD_ACCOUNT_ID}/adcreatives"

    creative_payload = {
        "access_token": ACCESS_TOKEN,
        "object_story_spec": {
            "page_id": "871672856033298",  # <-- Your Page ID here
            "video_data": {
                "video_id": video_id,
                "title": "My Video Creative",
                "message": "Uploaded from Streamlit + Flask"
            }
        }
    }

    creative_res = requests.post(
        creative_url,
        json=creative_payload
    ).json()

    creative_id = creative_res.get("id", "")

    return jsonify({
        "file_type": "video",
        "image_hash": "",
        "video_id": video_id,
        "thumbnail_id": thumbnail_id,
        "creative_id": creative_id
    })


@app.route("/")
def home():
    return "Meta Upload API Working!"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
