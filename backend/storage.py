import csv
import os

# Get this file folder: meta_upload_tool/backend/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one directory up → meta_upload_tool/
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Set results path correctly
RESULT_FILE = os.path.join(ROOT_DIR, "results", "creatives.csv")

# Ensure results/ exists
os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)


def save_result(filename, filetype, creative_id, hash_value, status):
    """Append creative upload result into CSV file."""
    file_exists = os.path.isfile(RESULT_FILE)

    with open(RESULT_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["filename", "type", "creative_id", "hash", "status"])

        writer.writerow([filename, filetype, creative_id, hash_value, status])
