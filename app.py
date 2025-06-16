
from flask import Flask, request, render_template_string, redirect
import sqlite3
import os
from video_downloader import download_from_url_or_profile
from uploader import upload_video

app = Flask(__name__)

# Load HTML dashboard
from dashboard_template import TEMPLATE

DB_PATH = "queue.db"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tiktok_input = request.form.get("tiktok_input")
        if tiktok_input:
            download_from_url_or_profile(tiktok_input)

    with sqlite3.connect(DB_PATH) as conn:
        queued = conn.execute("SELECT * FROM videos WHERE status = 'queued'").fetchall()

    return render_template_string(TEMPLATE, queued=queued)

@app.route("/force-upload/<int:video_id>", methods=["POST"])
def force_upload(video_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT * FROM videos WHERE id = ?", (video_id,)).fetchone()
        if row:
            video_path = os.path.join("static/processed", row[2])
            caption = row[3]
            upload_video(video_path, caption)
            conn.execute("UPDATE videos SET status = 'uploaded' WHERE id = ?", (video_id,))
    return redirect("/")
