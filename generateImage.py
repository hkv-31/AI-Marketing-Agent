#from google import genai
#from google.genai import types # type: ignore
from openai import OpenAI # type: ignore
#import argparse
#from datetime import datetime
import os
import json
#from typing import Callable, Optional, Dict, Any
import base64

# Load API keys from keys.json file
def load_api_keys():
    keys_path = "/Users/rushiljhaveri/Desktop/Coding/keys.json"
    try:
        with open(keys_path, 'r') as f:
            keys = json.load(f)
            #return keys.get("OPENAI_API_KEY"), keys.get("GEMINI_API_KEY")
            return keys.get("OPENAI_API_KEY")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading API keys: {e}")
        #return None, None
        return None

# Set API keys
#OPENAI_API_KEY, GEMINI_API_KEY = load_api_keys()
OPENAI_API_KEY = load_api_keys()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY if OPENAI_API_KEY else ""

def generate_image(prompt, image_paths):
    # API MODEL
    client = OpenAI()

    try:
        # Handle single or multiple images
        opened_files = []  # Track opened files to ensure we close them

        if isinstance(image_paths, list):
            if len(image_paths) == 1:
                # Single image case
                image = open(image_paths[0], "rb")
                opened_files.append(image)
            else:
                # Multiple images case - pass all images as a list
                image = []
                for path in image_paths:
                    file = open(path, "rb")
                    opened_files.append(file)
                    image.append(file)
        else:
            # Single image passed directly
            image = open(image_paths, "rb")
            opened_files.append(image)

        result = client.images.edit(
            model="gpt-image-1",
            image=image,  # This will be either a single image or a list of images
            prompt=prompt + "Ensure that all the content fits within the image, and that none of the content is cut off.",
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save the image to a file
        output_path = "generated.jpeg"
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        
        return {"image_base64": image_base64, "image_path": output_path}
    
    finally:
        # Close all opened files
        for file in opened_files:
            try:
                file.close()
            except:
                pass  # Ignore errors in cleanup

def main(prompt=None, image_paths=None):
    if prompt is None:
        print("Error: No prompt provided")
        return None
    if image_paths is None or (isinstance(image_paths, list) and len(image_paths) == 0):
        print("Error: No image paths provided")
        return None
    return generate_image(prompt, image_paths)

if __name__ == "__main__":
    main()