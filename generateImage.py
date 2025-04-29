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

def generate_image(prompt):
    # API MODEL
    client = OpenAI()

    #prompt = """
    #  Generate an image of a poster on saving water, showing a water bottle and a plant.
    #"""

    result = client.images.edit(
        model="gpt-image-1",
        image=open("/Users/rushiljhaveri/Desktop/Coding/AIAgents/stock.png", "rb"),
        prompt=prompt,
        output_format="jpeg",
        size="1024x1024",
        #size="1024x1024",
        #quality="high"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save the image to a file
    with open("generated.jpeg", "wb") as f:
        f.write(image_bytes)
    
    return image_bytes

def main(prompt=None):
    if prompt is None:
        print("Error: No prompt provided")
        return None
    return generate_image(prompt)

if __name__ == "__main__":
    main()