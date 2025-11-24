
"""
(Save uploaded file → Send to Meta → Save CSV → Return results)
Flask + Streamlit + cURL in the same CMD window.
Need 3 different CMD terminals:

"""
from flask import Flask, request, jsonify
import os
from meta_api import upload_image, upload_video
from storage import save_result

UPLOAD_FOLDER = "uploads/temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def is_video(filename):
    return filename.lower().endswith(".mp4")


def is_image(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))


@app.route("/", methods=["GET"])
def home():
    return {"message": "Backend is running!"}


@app.route("/upload", methods=["POST"])
def upload_files():
    try:
        files = request.files.getlist("files")
        if not files:
            return {"error": "No files uploaded"}, 400

        results = []

        for file in files:
            filename = file.filename
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            # Upload to Meta
            if is_image(filename):
                meta_res = upload_image(save_path)
                filetype = "image"
            else:
                meta_res = upload_video(save_path)
                filetype = "video"

            # Extract Creative ID + Hash
            creative_id = meta_res.get("id") or meta_res.get("video_id")
            hash_val = meta_res.get("hash")

            # Save to CSV
            save_result(filename, filetype, creative_id, hash_val, "success")

            results.append({
                "file": filename,
                "type": filetype,
                "creative_id": creative_id,
                "hash": hash_val,
                "raw_meta_response": meta_res
            })

        return jsonify({"status": "upload_complete", "results": results})

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)
