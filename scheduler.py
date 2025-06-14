import sqlite3
import time
import os
from datetime import datetime
from instagram_uploader import post_video

DB_PATH = "queue.db"
VIDEO_DIR = "static/processed"
POST_INTERVAL_MIN = int(os.getenv("POST_INTERVAL_MIN", "60"))

def schedule_all_pending():
    from threading import Thread
    Thread(target=run_scheduler, daemon=True).start()

def run_scheduler():
    while True:
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute("SELECT id, filename, caption FROM videos WHERE status = 'queued' ORDER BY id ASC LIMIT 1").fetchone()
            if row:
                vid_id, filename, caption = row
                filepath = os.path.join(VIDEO_DIR, filename)
                success = post_video(filepath, caption)
                if success:
                    now = datetime.utcnow().isoformat()
                    conn.execute("UPDATE videos SET status = 'posted', posted_time = ? WHERE id = ?", (now, vid_id))
        time.sleep(POST_INTERVAL_MIN * 60)