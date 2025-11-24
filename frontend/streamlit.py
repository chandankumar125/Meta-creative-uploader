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

        for f in uploaded_files:
            file_ext = f.name.lower()

            # Decide endpoint
            if file_ext.endswith((".jpg", ".jpeg", ".png")):
                endpoint = "http://localhost:5000/upload-image"
            elif file_ext.endswith(".mp4"):
                endpoint = "http://localhost:5000/upload-video"
            else:
                st.warning(f"Unsupported file: {f.name}")
                continue

            # Make request
            res = requests.post(
                endpoint,
                files={"file": (f.name, f.getvalue())}
            )

            # Try parsing JSON
            try:
                data = res.json()
            except:
                data = {"error": "Non-JSON backend response"}

            results.append({f.name: data})

            # -------------------------
            # CSV LOGIC
            # -------------------------

            # IMAGE CASE
            if "images" in data:
                info = list(data["images"].values())[0]
                image_hash = info.get("hash", "")
                csv_rows.append(["image", image_hash, ""])

            # VIDEO CASE (SAFE)
            else:
                inner = list(data.values())[0]

                if isinstance(inner, dict):
                    creative_id = inner.get("id", "")
                    csv_rows.append(["video", "", creative_id])
                else:
                    # Backend returned error string
                    csv_rows.append(["video", "", ""])

        # -------------------------
        # SAVE CSV (APPEND MODE)
        # -------------------------
        os.makedirs("results", exist_ok=True)
        csv_path = "results/creatives.csv"

        file_exists = os.path.isfile(csv_path)

        with open(csv_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["type", "image_hash", "creative_id"])

            writer.writerows(csv_rows)

        st.success("Upload Complete!")
        st.json(results)
        st.info("Saved CSV → results/creatives.csv (appended)")


