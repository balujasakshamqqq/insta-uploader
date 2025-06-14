from instagrapi import Client
import os

# Load environment variables if needed
USERNAME = "cararoma_"
PASSWORD = "Saksham@06"
SESSION_FILE = "session.json"

# Initialize the client
cl = Client()

# Try to load session if exists
if os.path.exists(SESSION_FILE):
    print("Loading session...")
    cl.load_settings(SESSION_FILE)

# Login (this will reuse session if available)
try:
    cl.login(USERNAME, PASSWORD)
    print("Logged in successfully.")
    cl.dump_settings(SESSION_FILE)  # Save updated session
except Exception as e:
    print("Login failed:", e)
    exit()

# Upload function
def post_video(video_path, caption):
    try:
        print(f"Uploading: {video_path}")
        media = cl.clip_upload(video_path, caption)
        print("✅ Upload successful:", media.dict().get("pk"))
    except Exception as e:
        print("❌ Upload failed:", e)

# Example usage
if __name__ == "__main__":
    video_file = "video.mp4"  # Replace with your downloaded TikTok video
    caption_text = "🔥 Trending Product - Now Live on Our Store!"
    post_video(video_file, caption_text)
