How this will works
1. Project Structure
meta_upload_tool/
│
├── backend/
│   ├── app.py
│   ├── meta_api.py
│   ├── storage.py
│   ├── config.py
│   ├── requirements.txt
│
├── uploads/
│   ├── temp/
│
├── frontend/
│   ├── streamlit.py
│
├── results/
│   ├── creatives.csv
│
└── README.md

2. Install Requirements and env
python -m venv venv
.\venv\Scripts\activate

cd meta_upload_tool/backend
pip install -r requirements.txt

3. Run Backend (Flask) python .\backend\app.py or 

cd meta_upload_tool/backend
python app.py
Backend runs at:
👉 http://127.0.0.1:5000

4. Frontend requirements: In other terminal
cd meta_upload_tool/frontend
Pip install streamlit   or (without pyarrow) pip install streamlit --no-cache-dir --only-binary=:all:

streamlit run streamlit.py
Streamlit UI launches at:
👉 http://localhost:8501

This UI will:
Upload images/videos
Send them to Flask backend
Show Creative ID + Hash
Display raw API response


## Upload Flow (How System Works)
Streamlit UI → Flask Backend → Meta API → CSV
1. User uploads media in Streamlit
⬇
2. UI sends files to Flask /upload
⬇
3. Flask saves files to /uploads/temp/
⬇
4. Backend calls:

/adimages → for JPG/PNG

/advideos → for MP4
⬇

5. Meta returns:
creative ID
image/video hash
⬇

6. Backend writes results to:
results/creatives.csv

7. Streamlit displays results to user


# Output: Download as results
Image/videos Upload → CSV
file type  creative_id	image_hash	status
