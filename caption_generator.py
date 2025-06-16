
import re
import random

def extract_keywords(filename):
    words = re.findall(r'\w+', filename.lower())
    filtered = [w for w in words if len(w) > 3 and w.isalpha()]
    return list(set(filtered))[:5]

def generate_caption(filename):
    keywords = extract_keywords(filename)
    intro_lines = [
        "🔥 Just Dropped!",
        "🎥 Must-Watch Now!",
        "🚀 Going Viral!",
        "✨ You Can’t Miss This!",
        "🎬 Trending on Insta!",
        "💥 Watch Till the End!"
    ]
    intro = random.choice(intro_lines)
    hashtags = " ".join([f"#{w}" for w in keywords])
    return f"{intro}\n{hashtags} #viral #foryou #reels"
