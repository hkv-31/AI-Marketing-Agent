# Instabot.py

import os
import sys
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice

# Config
SESSION_FILE = "insta_session.json"
testing_mode = False

def login(username, password):
    cl = Client()

    def challenge_code_handler(choice: ChallengeChoice):
        return input(f"Enter the code sent via **{choice.name}**: ")

    cl.challenge_code_handler = challenge_code_handler

    try:
        if os.path.isfile(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
            print("✅ Session loaded and login succeeded")
        else:
            cl.login(username, password)
            print("✅ Fresh login succeeded")
    except Exception as e:
        print(f"⚠️ Login failed ({e}); retrying fresh login…")
        cl.login(username, password)

    cl.dump_settings(SESSION_FILE)
    return cl

def upload_photo(username, password, photo_path, caption):
    if testing_mode:
        print(f"🧪 [Testing Mode] Would have posted {photo_path} with caption: {caption}")
        return "DummyMediaID123"

    if not os.path.isfile(photo_path):
        raise FileNotFoundError(f"Image not found at: {photo_path}")
    if not photo_path.lower().endswith((".jpg", ".jpeg")):
        raise ValueError("instagrapi only supports .jpg/.jpeg files")

    cl = login(username, password)
    media = cl.photo_upload(photo_path, caption=caption)
    print(f"✅ Photo uploaded successfully! Media ID: {media.pk}")
    return media.pk

def main():
    if len(sys.argv) < 5:
        print("Usage: python Instabot.py username password photo_path caption")
        return

    username = sys.argv[1]
    password = sys.argv[2]
    photo_path = sys.argv[3]
    caption = sys.argv[4]
    upload_photo(username, password, photo_path, caption)

if __name__ == "__main__":
    main()
