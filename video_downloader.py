import os
import subprocess
import hashlib
import sqlite3
import re
from datetime import datetime
from caption_generator import generate_caption
from duplicate_checker import is_duplicate, register_hash

DB_PATH = "queue.db"
DOWNLOAD_DIR = "static/processed"

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def compute_sha256(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def save_to_db(source, filename, caption, hash_val):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO videos (source, filename, caption, status, hash, scheduled_time, posted_time)
            VALUES (?, ?, ?, 'queued', ?, NULL, NULL)
        """, (source, filename, caption, hash_val))

def download_from_url_or_profile(input_str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    if "tiktok.com" in input_str:
        command = ["yt-dlp", input_str, "-P", DOWNLOAD_DIR, "-o", "%(title).40s.%(ext)s"]
    else:
        input_str = input_str.strip().lstrip("@")
        command = ["yt-dlp", f"https://www.tiktok.com/@{input_str}", "-P", DOWNLOAD_DIR, "-o", "%(title).40s.%(ext)s"]

    subprocess.run(command, capture_output=True)

    for file in os.listdir(DOWNLOAD_DIR):
        if file.endswith(".mp4"):
            filepath = os.path.join(DOWNLOAD_DIR, file)
            hash_val = compute_sha256(filepath)
            if is_duplicate(hash_val):
                continue
            caption = generate_caption(file)
            register_hash(hash_val)
            save_to_db(input_str, file, caption, hash_val)