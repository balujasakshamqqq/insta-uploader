def download_from_url_or_profile(input_str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    print("📥 Starting download for:", input_str)

    # Build yt-dlp command
    if "tiktok.com" in input_str:
        command = [
            "yt-dlp",
            "-f", "mp4/best",  # More compatible fallback
            input_str,
            "-P", DOWNLOAD_DIR,
            "-o", "%(title).40s.%(ext)s"
        ]
    else:
        input_str = input_str.strip().lstrip("@")
        command = [
            "yt-dlp",
            "-f", "mp4/best",
            f"https://www.tiktok.com/@{input_str}",
            "-P", DOWNLOAD_DIR,
            "-o", "%(title).40s.%(ext)s"
        ]

    result = subprocess.run(command, capture_output=True, text=True)

    print("🧾 yt-dlp stdout:", result.stdout)
    print("❗ yt-dlp stderr:", result.stderr)

    found_video = False

    for file in os.listdir(DOWNLOAD_DIR):
        filepath = os.path.join(DOWNLOAD_DIR, file)

        # Skip non-video files
        if not file.endswith(".mp4"):
            if file.endswith(".m4a"):
                os.remove(filepath)  # Optional cleanup
            continue

        found_video = True
        print(f"✅ Found video: {file}")

        hash_val = compute_sha256(filepath)
        print(f"🔑 Hash: {hash_val}")

        if is_duplicate(hash_val):
            print("⛔ Skipping duplicate:", file)
            continue

        caption = generate_caption(file)
        register_hash(hash_val)
        save_to_db(input_str, file, caption, hash_val)
        print("✅ Video queued:", file)

    if not found_video:
        print("⚠️ No new videos found in", DOWNLOAD_DIR)
