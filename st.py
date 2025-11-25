"""
output csv formate: type,image_hash,creative_id
if you upload same image again and again and perviously already created image_hash of that image, will not create dublicacy in results csv. 
image
problems: creative id not storing, previous stored in csv data lost

"""
import streamlit as st
import requests
import csv
import os

st.title("Meta Creative Uploader")

uploaded_files = st.file_uploader(
    "Upload Images / Videos (JPG / PNG / MP4)",
    accept_multiple_files=True
)

if st.button("Start Upload"):
    if not uploaded_files:
        st.error("Please select at least one file!")
    else:
        results = []
        csv_rows = []
        # TRACK DUPLICATES
        seen_hashes = set()
        seen_creative_ids = set()

        for f in uploaded_files:
            file_ext = f.name.lower()

            # Select endpoint based on file type
            if file_ext.endswith((".jpg", ".jpeg", ".png")):
                endpoint = "http://localhost:5000/upload-image"
            elif file_ext.endswith(".mp4"):
                endpoint = "http://localhost:5000/upload-video"
            else:
                st.warning(f"Unsupported file: {f.name}")
                continue

            # Send file to backend
            res = requests.post(
                endpoint,
                files={"file": (f.name, f.getvalue())}
            )

            try:
                data = res.json()
            except:
                data = {"error": "Non-JSON backend response"}

            results.append({f.name: data})

            # -------- CSV Handling --------
            # Image Response
            if "images" in data:
                info = list(data["images"].values())[0]
                image_hash = info.get("hash", "")
                csv_rows.append(["image", image_hash, ""])

            # Video Response
            elif "videos" in data:
                info = list(data.values())[0]
                creative_id = info.get("id", "")
                csv_rows.append(["video", "", creative_id])
            
            
        # -------- SAVE CSV --------
        os.makedirs("results", exist_ok=True)
        csv_path = "results/creatives.csv"

        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["type", "image_hash", "creative_id"])
            writer.writerows(csv_rows)

        st.success("Upload Complete!")
        st.json(results)
        st.info("Saved → results/creatives.csv")
