### **README.md**

```markdown
# Meta Upload API

A FastAPI-based API to upload images and videos to Meta (Facebook) Ads, and retrieve video thumbnails using the Facebook Graph API (v24.0).  
The API includes Swagger documentation for easy testing.

---

## Features

- Upload image to Meta Ads → returns `image_hash`.
- Upload video to Meta Ads → returns `video_creative_id`.
- Retrieve thumbnails for a video → returns list of thumbnails with `id`, `uri`, `height`, `width`, and `is_preferred`.

---

## Folder Structure

```

meta_upload_api/
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
├── temp/             # Temporary folder for uploads (auto-created)
├── .gitignore        # Ignore temporary files, env, etc.
└── README.md

````

---

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Requests
- Python-Multipart

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/meta_upload_api.git
cd meta_upload_api
````

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your Meta Ads credentials in `main.py`:

```python
AD_ACCOUNT_ID = "YOUR_AD_ACCOUNT_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
```

---

## Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

1. **Upload Image**

   * `POST /upload-image`
   * Form-data: `file` (image)
   * Returns: `image_hash`

2. **Upload Video**

   * `POST /upload-video`
   * Form-data: `file` (video), optional `title`
   * Returns: `video_creative_id`

3. **Get Video Thumbnails**

   * `GET /video-thumbnails?video_id=<VIDEO_ID>`
   * Returns: Array of thumbnail objects with `id`, `uri`, `height`, `width`, `scale`, `is_preferred`

---

## Notes

* All temporary uploads are stored in `temp/` and removed after processing.
* Ensure your access token has proper permissions (`ads_management`, `business_management`) to access video thumbnails or upload ads.
* Use Graph API v24.0 endpoints to ensure compatibility.

---