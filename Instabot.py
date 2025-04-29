import os
import sys
from instagrapi import Client #type: ignore
from instagrapi.mixins.challenge import ChallengeChoice #type: ignore

def post_to_instagram(username, password, photo_path, caption):
    # ——— CONFIG ———
    SESSION_FILE = "/Users/rushiljhaveri/Desktop/Coding/AIAgents/TrendlyAI/resources/insta_session.json" 
    
    # ——— PRE-CHECKS ———
    if not os.path.isfile(photo_path):
        raise FileNotFoundError(f"Image not found at: {photo_path}")
    if not photo_path.lower().endswith((".jpg", ".jpeg")):
        raise ValueError("instagrapi only supports .jpg/.jpeg files")
    
    # ——— CLIENT SETUP ———
    cl = Client()
    
    # **Custom challenge handler** to prompt you for 2FA or checkpoint codes
    def challenge_code_handler(username: str, choice: ChallengeChoice):
        print(f"🔒 Challenge for user {username} via {choice.name}")
        return input(f"Enter the code sent via {choice.name}: ")
    
    cl.challenge_code_handler = challenge_code_handler
    
    # ——— LOGIN (load or fresh) ———
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
    
    # **Save** the session for next runs
    cl.dump_settings(SESSION_FILE)
    
    # ——— UPLOAD PHOTO ———
    try:
        media = cl.photo_upload(photo_path, caption=caption)
        print(f"✅ Photo uploaded successfully! Media ID: {media.pk}")
        return True, f"Photo uploaded successfully! Media ID: {media.pk}"
    except Exception as e:
        error_message = f"Failed to upload photo: {str(e)}"
        print(f"❌ {error_message}")
        return False, error_message

if __name__ == "__main__":
    # For command-line usage
    if len(sys.argv) < 5:
        print("Usage: python Instabot.py [username] [password] [photo_path] [caption]")
        sys.exit(1)
        
    username = sys.argv[1]
    password = sys.argv[2]
    photo_path = sys.argv[3]
    caption = sys.argv[4]
    
    post_to_instagram(username, password, photo_path, caption)
