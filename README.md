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

# for image: 
curl --location --globoff "https://graph.facebook.com/v19.0/act_1324697116076599/adimages" ^
--form "access_token=EAAQeYqt2zH4BQPzq34..." ^
--form "file=@C:/Users/Adsparkx/Downloads/pexels-ron-lach-9586529.png"
# 
curl --location --globoff "https://graph.facebook.com/v19.0/act_1324697116076599/adimages" ^
--form "access_token=EAAQeYqt2zH4BQPzq34ZA149r3oXcwXRr40zBu14Q0fi3aR2iAY3t3OJPmvKjzUHxyNqsn0ZCFEKepADXLYotDTxZBhBpLj7o1y9lsHVFcwzxg1FlXNM9reBQTr69VinyepwthQSGLy5D7y2YGZAASWZChlGRVAqyNlj0Fbph7wlLddfgqPxRCCCNWTNGU4LdTCNRw" ^
--form "file=@C:/Users/Adsparkx/Downloads/pexels-ron-lach-9586529.png"

# for videos
curl --location "https://graph.facebook.com/v19.0/act_1324697116076599/advideos" ^
--form "access_token=EAAQeYqt2zH4BQPzq34..." ^
--form "file=@C:/Users/Adsparkx/Downloads/8028803-uhd_2160_3840_24fps.mp4" ^
--form "title=Anything"

# curl --location "https://graph.facebook.com/v19.0/act_1324697116076599/advideos" ^
--form "access_token=EAAQeYqt2zH4BQPzq34ZA149r3oXcwXRr40zBu14Q0fi3aR2iAY3t3OJPmvKjzUHxyNqsn0ZCFEKepADXLYotDTxZBhBpLj7o1y9lsHVFcwzxg1FlXNM9reBQTr69VinyepwthQSGLy5D7y2YGZAASWZChlGRVAqyNlj0Fbph7wlLddfgqPxRCCCNWTNGU4LdTCNRw" ^
--form "file=@C:/Users/Adsparkx/Downloads/8028803-uhd_2160_3840_24fps.mp4" ^
--form "title=Anything"




Image Upload → CSV
| filename | type  | image_hash | status |

Video Upload → CSV
filename	type  creative_id	video_hash	status
