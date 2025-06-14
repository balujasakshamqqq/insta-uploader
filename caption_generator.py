import re

def extract_keywords(filename):
    words = re.findall(r'\w+', filename.lower())
    filtered = [w for w in words if len(w) > 3 and w.isalpha()]
    return list(set(filtered))[:5]

def generate_caption(filename):
    keywords = extract_keywords(filename)
    base_caption = "🚀 Trending Now on Insta! "
    hashtags = " ".join([f"#{w}" for w in keywords])
    return f"{base_caption}\n{hashtags} #viral #foryou #reels"