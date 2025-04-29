import os
import sys
from instagrapi import Client #type: ignore
from instagrapi.mixins.challenge import ChallengeChoice #type: ignore

# ——— CONFIG ———
USERNAME     = "fybba.a.ppa"
PASSWORD     = "rushiljhaveri3"
PHOTO_PATH   = sys.argv[1] if len(sys.argv) > 1 else "/Users/rushiljhaveri/Desktop/Coding/AIAgents/TrendlyV2/generated_output.jpeg"
CAPTION      = "THIS IS A COOL POSTER #COOL #POSTER"
SESSION_FILE = "insta_session.json" 

# ——— PRE-CHECKS ———
if not os.path.isfile(PHOTO_PATH):
    raise FileNotFoundError(f"Image not found at: {PHOTO_PATH}")
if not PHOTO_PATH.lower().endswith((".jpg", ".jpeg")):
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
        cl.login(USERNAME, PASSWORD)
        print("✅ Session loaded and login succeeded")
    else:
        cl.login(USERNAME, PASSWORD)
        print("✅ Fresh login succeeded")
except Exception as e:
    print(f"⚠️ Login failed ({e}); retrying fresh login…")
    cl.login(USERNAME, PASSWORD)

# **Save** the session for next runs
cl.dump_settings(SESSION_FILE)

# ——— UPLOAD PHOTO ———
media = cl.photo_upload(PHOTO_PATH, caption=CAPTION)
print(f"✅ Photo uploaded successfully! Media ID: {media.pk}")
