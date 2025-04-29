# webSearch.py

from openai import OpenAI # type: ignore
import os
import json
from google import genai # type: ignore
from google.genai import types # type: ignore

# Load API keys dynamically

def load_api_keys():
    keys_path = "keys.json"
    try:
        with open(keys_path, 'r') as f:
            keys = json.load(f)
            return keys.get("OPENAI_API_KEY"), keys.get("GEMINI_API_KEY")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading API keys: {e}")
        return None, None

# Set API keys
OPENAI_API_KEY, GEMINI_API_KEY = load_api_keys()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY if OPENAI_API_KEY else ""

# Real or dummy testing
testing_mode = False

def trend_search():
    if testing_mode:
        print("🧪 [Testing Mode] Dummy trend generated.")
        return "Dummy trend: Funny memes about futuristic food delivery."

    # Verify API keys are available
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing or invalid. Please check your keys.json file.")
    
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is missing or invalid. Please check your keys.json file.")

    # Create client with API key explicitly
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    web_search_prompt = (
        "Scan the internet for the latest viral and emerging trends in food marketing, "
        "focusing on memes and humor-driven content. Identify patterns from brand memes, "
        "humorous food advertisements, parody campaigns, satirical influencer content, trending food jokes, "
        "and meme-based guerrilla marketing tactics."
    )

    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        tools=[{
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            },
            "search_context_size": "high"
        }],
        input=web_search_prompt,
    )

    output = response.output_text

    image_prompt_creation_prompt = "Create a prompt for an image generation model to generate an image that captures the essence of the trend described in the following text: " + output
    system_prompt = "You are a creative and imaginative image prompt creator. Your task is to generate a detailed and creative prompt for an image generation model that captures the essence of the trend described in the input text. The prompt should be concise, engaging, and evocative, encouraging the model to create a visually appealing and culturally relevant image."

    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash-thinking-exp",
        config=types.GenerateContentConfig(
        system_instruction=system_prompt),
        contents=[image_prompt_creation_prompt]
    )

    output = response.text
    print("✅ Trend search completed.")
    return output

def main():
    trend = trend_search()
    print("========TREND OUTPUT=========")
    print(trend)

if __name__ == "__main__":
    main()
