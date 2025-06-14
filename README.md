# 📲 Instagram Reels Auto-Uploader (TikTok → Instagram)

Automatically download TikTok videos by link or full profile, generate smart captions, detect duplicates, and auto-post to Instagram Reels.

### 🚀 Deployment on Render
1. Upload code to GitHub
2. Create new Web Service on [https://render.com](https://render.com)
3. Add these environment variables:
   - IG_USERNAME
   - IG_PASSWORD
   - POST_INTERVAL_MIN

**Build command:** pip install -r requirements.txt  
**Start command:** gunicorn app:app --bind 0.0.0.0:$PORT

Then open the Render-provided link to access your dashboard.
