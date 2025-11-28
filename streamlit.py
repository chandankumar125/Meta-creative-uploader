import streamlit as st
import requests
import csv
import os
import json


# -----------------------------
# Safe JSON Loader
# -----------------------------
def safe_json(res):
    try:
        return res.json()
    except:
        return {
            "error": "Non-JSON backend response",
            "status": res.status_code,
            "text": res.text[:300]
        }


# -----------------------------
# Safe CSV file opener
# -----------------------------
def safe_open_csv(base_path):
    folder = os.path.dirname(base_path)
    name = os.path.basename(base_path)
    base, ext = os.path.splitext(name)

    attempt = 0
    path = base_path

    while True:
        try:
            return open(path, "a", newline="", encoding="utf-8"), path
        except PermissionError:
            attempt += 1
            path = os.path.join(folder, f"{base}_{attempt}{ext}")


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("Meta Creative Uploader")

uploaded_files = st.file_uploader(
    "Upload Images / Videos (JPG / PNG / MP4)",
    accept_multiple_files=True
)

if st.button("Start Upload"):

    if not uploaded_files:
        st.error("Please select at least one file!")
        st.stop()

    results = []
    csv_rows = []

    seen_hashes = set()
    seen_videos = set()

    progress = st.progress(0)
    total = len(uploaded_files)

    for idx, f in enumerate(uploaded_files):
        progress.progress((idx + 1) / total)

        filename = f.name.lower()

        # Detect type
        if filename.endswith(("jpg", "jpeg", "png")):
            endpoint = "http://localhost:5000/upload-image"
            file_type = "image"
        elif filename.endswith("mp4"):
            endpoint = "http://localhost:5000/upload-video"
            file_type = "video"
        else:
            st.warning(f"Unsupported file: {f.name}")
            continue

        # -----------------------
        # API REQUEST
        # -----------------------
        try:
            res = requests.post(endpoint, files={"file": (f.name, f.getvalue())})
            data = safe_json(res)
        except Exception as e:
            data = {"error": "Request failed", "detail": str(e)}

        # Save raw result
        results.append({f.name: data})

        # Show errors
        if "error" in data:
            st.error(f"Error uploading {f.name}")
            st.json(data)
            continue

        # -----------------------
        # Extract fields safely
        # -----------------------
        image_hash = (
            data.get("image_hash")
            or data.get("hash")
            or data.get("md5")
            or ""
        )

        video_id = data.get("video_id") or data.get("id") or ""
        thumbnail_id = data.get("thumbnail_id") or data.get("thumb_id") or ""
        creative_id = (
            data.get("creative_id") or
            data.get("id") or
            data.get("creative") or
            ""
        )

        # -----------------------
        # Duplicate Protection
        # -----------------------
        if file_type == "image":
            if image_hash in seen_hashes:
                continue
            seen_hashes.add(image_hash)

            csv_rows.append([
                "image",
                image_hash,
                "",
                "",
                ""
            ])

        elif file_type == "video":
            if video_id in seen_videos:
                continue
            seen_videos.add(video_id)

            csv_rows.append([
                "video",
                image_hash,
                video_id,
                thumbnail_id,
                creative_id
            ])

    # -----------------------
    # SAVE CSV
    # -----------------------
    os.makedirs("results", exist_ok=True)
    csv_path = "results/creatives.csv"

    is_new = not os.path.exists(csv_path)
    file, actual_path = safe_open_csv(csv_path)

    with file:
        writer = csv.writer(file)
        if is_new:
            writer.writerow(
                ["file_type", "image_hash", "video_id", "thumbnail_id", "creative_id"]
            )
        writer.writerows(csv_rows)

    # Output
    st.success("Upload Complete!")
    st.json(results)
    st.info(f"Saved to: {actual_path}")
