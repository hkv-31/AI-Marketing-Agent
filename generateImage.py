# generateImage.py

from openai import OpenAI # type: ignore
import os
import json
import base64

# Load API keys
def load_api_keys():
    keys_path = "keys.json"
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

# Testing mode flag
testing_mode = False

def generate_image(prompt, base_image_path=None):
    client = OpenAI()
    if testing_mode:
        print("🧪 [Testing Mode] Returning dummy image bytes.")
        return b"FAKE_IMAGE_BYTES"

    if base_image_path:
        # Edit existing image
        with open(base_image_path, "rb") as img_file:
            result = client.images.edit(
                model="gpt-image-1",
                image=img_file,
                prompt=prompt,
                size="1024x1024"
            )
    else:
        # Generate from scratch
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save generated image
    output_file = "generated_output.jpeg"
    with open(output_file, "wb") as f:
        f.write(image_bytes)
    
    return image_bytes

def main(prompt=None, base_image_path=None):
    if prompt is None:
        print("Error: No prompt provided")
        return None
    return generate_image(prompt, base_image_path)

if __name__ == "__main__":
    sample_prompt = "A futuristic pizza meme for a Gen-Z audience."
    main(sample_prompt)
