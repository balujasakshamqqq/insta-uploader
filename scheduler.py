import time
import threading
import os
import sqlite3
from instagrapi import Client
from datetime import datetime

DB_PATH = "queue.db"
DOWNLOAD_DIR = "static/processed"

def upload_one_video():
    with sqlite3.connect(DB_PATH) as conn:
        video = conn.execute("SELECT * FROM videos WHERE status = 'queued' ORDER BY id LIMIT 1").fetchone()
        if video:
            video_id, source, filename, caption, status, hash_val, _, _ = video
            video_path = os.path.join(DOWNLOAD_DIR, filename)

            print("📤 Uploading:", filename)
            cl = Client()
            cl.load_settings("sessions.json")
            cl.login_by_sessionid(os.getenv("INSTAGRAM_SESSIONID"))

            try:
                result = cl.clip_upload(video_path, caption=caption)
                print("✅ Upload successful:", result.dict().get("pk"))
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn.execute("UPDATE videos SET status = 'posted', posted_time = ? WHERE id = ?", (now, video_id))
                conn.commit()
            except Exception as e:
                print("❌ Upload failed:", e)

def run_scheduler():
    while True:
        upload_one_video()
        print("⏳ Waiting 30 minutes...")
        time.sleep(1800)

def start_background_scheduler():
    t = threading.Thread(target=run_scheduler)
    t.daemon = True
    t.start()
