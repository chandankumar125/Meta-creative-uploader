import streamlit as st
import requests
import csv
import os
from datetime import datetime


# Safe CSV open function to avoid file locking errors
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

# UI
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

    # Track duplicates
    seen_hashes = set()
    seen_creative_ids = set()

    for f in uploaded_files:
        file_ext = f.name.lower()

        # Pick endpoint
        if file_ext.endswith((".jpg", ".jpeg", ".png")):
            endpoint = "http://localhost:5000/upload-image"
        elif file_ext.endswith(".mp4"):
            endpoint = "http://localhost:5000/upload-video"
        else:
            st.warning(f"Unsupported file: {f.name}")
            continue

        # Backend request
        try:
            res = requests.post(
                endpoint,
                files={"file": (f.name, f.getvalue())}
            )
            data = res.json()
        except:
            data = {"error": "Non-JSON backend response"}

        results.append({f.name: data})

        # IMAGE
        if file_ext.endswith((".jpg", ".jpeg", ".png")):
            image_hash = ""
            if "images" in data and isinstance(data["images"], dict):
                first_key = next(iter(data["images"]))
                image_hash = data["images"][first_key].get("hash", "")
            #if image_hash and image_hash in seen_hashes:
            #    continue
            #seen_hashes.add(image_hash)
            csv_rows.append(["image", "", image_hash])  # [file type, creative_id, image_hash]

        # VIDEO
        elif file_ext.endswith(".mp4"):
            print('video section')
            print('data: in the video sec:', data)
            creative_id = data['id']
            
            # Ensure the file is present in the data dictionary and it's in the expected format
            if f.name in data and isinstance(data[f.name], dict):
                # Extract the creative_id directly
                print('test:', creative_id)
                creative_id = data[f.name].get("id", "")
            
            # Skip if the creative_id is already processed
            if creative_id and creative_id in seen_creative_ids:
                print('already exits')
                continue
            
            # Add the creative_id to the set of seen IDs
            seen_creative_ids.add(creative_id)
            
            # Append to csv_rows with the extracted creative_id
            csv_rows.append(["video", creative_id, ""])  # [file type, creative_id, image_hash]

    # SAVE CSV (SAFE)
    os.makedirs("results", exist_ok=True)
    csv_path = "results/creatives.csv"

    file, path_used = safe_open_csv(csv_path)
    new_file = not os.path.exists(path_used)
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with file:
        writer = csv.writer(file)
        writer.writerow(["file type", "creative_id", "image_hash"])
        # WRITE HEADER FOR NEW FILE
        if new_file:
            writer.writerow(["file type", "creative_id", "image_hash"])
        writer.writerows(csv_rows)



    st.success("Upload Complete!")
    st.json(results)
    st.info(f"Saved to result/creatives.csv → {path_used}")
