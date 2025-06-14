from flask import Flask, request, render_template_string, redirect
import os
from dotenv import load_dotenv
import sqlite3
from video_downloader import download_from_url_or_profile
from scheduler import schedule_all_pending
# --- TEMPORARY DATABASE INITIALIZATION ---
import sqlite3

conn = sqlite3.connect("database.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued'
)
""")
conn.commit()
conn.close()
# --- END DB INIT ---


app = Flask(__name__)
load_dotenv()

DB_PATH = 'queue.db'
os.makedirs("static/processed", exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS videos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            source TEXT,
                            filename TEXT,
                            caption TEXT,
                            status TEXT,
                            hash TEXT,
                            scheduled_time TEXT,
                            posted_time TEXT
                        )''')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tiktok_input = request.form.get("tiktok_input")
        if tiktok_input:
            download_from_url_or_profile(tiktok_input)
            schedule_all_pending()
            return redirect("/")
    with sqlite3.connect(DB_PATH) as conn:
        queued = conn.execute("SELECT * FROM videos WHERE status = 'queued'").fetchall()
        posted = conn.execute("SELECT * FROM videos WHERE status = 'posted'").fetchall()
    return render_template_string(TEMPLATE, queued=queued, posted=posted)

TEMPLATE = """<!doctype html>
<title>Instagram Uploader Dashboard</title>
<h2>Upload TikTok Link or Profile</h2>
<form method=post>
  <input type=text name=tiktok_input style="width:400px" placeholder="TikTok link or username">
  <input type=submit value=Submit>
</form>

<h3>🕒 Pending Uploads</h3>
<ul>
{% for row in queued %}
  <li><b>{{ row[2] }}</b> — {{ row[3] }}</li>
{% else %}
  <li>No videos in queue.</li>
{% endfor %}
</ul>

<h3>✅ Posted Videos</h3>
<ul>
{% for row in posted %}
  <li><b>{{ row[2] }}</b> — {{ row[7] }}</li>
{% else %}
  <li>No videos posted yet.</li>
{% endfor %}
</ul>"""

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
