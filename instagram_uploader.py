import os
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(USERNAME, PASSWORD)

def post_video(filepath, caption):
    try:
        cl.clip_upload(path=filepath, caption=caption)
        return True
    except Exception as e:
        print(f"[❌] Upload failed: {e}")
        return False