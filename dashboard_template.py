
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Auto-Uploader</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f6f6f6; padding: 20px; }
        h1 { color: #333; }
        .video-list { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 8px #ccc; }
        .video-item { margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
        .caption { font-size: 0.9em; color: #666; }
        .btn { padding: 5px 10px; background: #4CAF50; color: white; border: none; cursor: pointer; border-radius: 4px; }
        .btn:hover { background: #45a049; }
        form { margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>📥 Instagram Video Queue</h1>
    <form method="POST">
        <input type="text" name="tiktok_input" placeholder="Paste TikTok Link or @username" size="50" required>
        <button type="submit" class="btn">Download & Queue</button>
    </form>

    <div class="video-list">
        <h2>Queued Videos ({{ queued|length }})</h2>
        {% if queued %}
            {% for vid in queued %}
            <div class="video-item">
                <strong>{{ vid[2] }}</strong><br>
                <div class="caption">{{ vid[3] }}</div>
                Scheduled: {{ vid[5] or "To be scheduled" }}<br>
                <form action="/force-upload/{{ vid[0] }}" method="POST" style="margin-top:5px;">
                    <button type="submit" class="btn">Force Upload</button>
                </form>
            </div>
            {% endfor %}
        {% else %}
            <p>No videos in queue.</p>
        {% endif %}
    </div>
</body>
</html>
"""
