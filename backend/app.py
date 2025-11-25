from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN="EAAQeYqt2zH4BQMNm9RRLNJAuAfnqQ72wfdNFJ2WxbL9XhPlHeBVo41OjpTvkZAEIN0ySZCyHf3lC2f1YiQJ32itKRQXq6Yz2xt5RNsKk2RXryCEGxhSbAaUgLaLwKrVL7uu11scZBnSRWoLvqPkwZBePpDhz2xzMUjUads91cEH6bYZBwkO5ZBqtDavfL0nZARjSz3z"
AD_ACCOUNT_ID="1324697116076599"


# -------------------------------
# 1. Upload Image to Meta
# -------------------------------
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    # Save temporarily
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
    return jsonify(response.json())


# -------------------------------
# 2. Upload Video to Meta
# -------------------------------
@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    file = request.files['file']
    # Save temporarily
    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    url = f"https://graph.facebook.com/v19.0/act_{AD_ACCOUNT_ID}/advideos"

    with open(temp_path, 'rb') as f:
        response = requests.post(
            url,
            files={"file": f},
            data={
                "access_token": ACCESS_TOKEN,
                "title": "Uploaded via Flask"
            }
        )

    os.remove(temp_path)
    return jsonify(response.json())


@app.route("/")
def home():
    return "Meta Upload API Working!"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
