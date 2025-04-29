from google import genai
from google.genai import types # type: ignore
from openai import OpenAI # type: ignore
#import argparse
#from datetime import datetime
import os
import json
#from typing import Callable, Optional, Dict, Any
#import base64

# Load API keys from keys.json file
def load_api_keys():
    keys_path = "/Users/rushiljhaveri/Desktop/Coding/keys.json"
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

def rag_website(brand_url):
    if not brand_url:
        return "No website URL provided."
    
    try:
        openai_client = OpenAI()

        # Read the RAG prompt
        try:
            with open('/Users/rushiljhaveri/Desktop/Coding/AIAgents/TrendlyAI/resources/rag_prompt.txt', 'r') as f:
                rag_prompt = f.read().strip()
        except Exception as e:
            print(f"Error reading RAG prompt: {e}")
            return "Error reading RAG prompt."

        rag_prompt = rag_prompt.replace("{{Website_link}}", brand_url)
        
        print(f"Sending RAG request for website: {brand_url}")
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
            input=rag_prompt,
        )
        
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'output_text'):
            return response.output_text
        else:
            print("RAG response has neither 'text' nor 'output_text' attribute")
            print("Response attributes:", dir(response))
            return f"Website summary unavailable. Please check the URL: {brand_url}"
            
    except Exception as e:
        print(f"Exception in rag_website: {e}")
        return f"Error processing website: {str(e)}"

def trend_search(brand_name, brand_desription, brand_website, product_type):
    openai_client = OpenAI()

    # Load the search prompt from the file
    try:
        with open('/Users/rushiljhaveri/Desktop/Coding/AIAgents/TrendlyAI/resources/search_prompt.txt', 'r') as f:
            web_search_prompt = f.read().strip()
    except Exception as e:
        print(f"Error loading search prompt: {e}")
        raise Exception(f"Could not load search prompt: {e}")

    try:
        brand_brief = brand_desription
        if brand_website:
            print(f"Fetching website data for: {brand_website}")
            website_info = rag_website(brand_website)
            brand_brief = brand_desription + "\n" + website_info
        else:
            print("No website provided, skipping RAG")
    except Exception as e:
        print(f"Error with RAG website: {e}")
        brand_brief = brand_desription
        print("Using only brand description without website data")

    print(f"Creating prompt with: Brand: {brand_name}, Brief: {brand_brief[:100]}..., Product: {product_type}")
    
    web_search_prompt = web_search_prompt.replace("{{brand_name}}", brand_name)
    web_search_prompt = web_search_prompt.replace("{{brand_brief}}", brand_brief)
    web_search_prompt = web_search_prompt.replace("{{product_type}}", product_type)

    try:
        print("Sending request to OpenAI API...")
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
        
        print("Got response from OpenAI API")
        output = response.output_text
        print("Output type:", type(output))
        print("Output sample:", output[:100] if output else "Empty output")
        
        # For debugging
        if not output:
            print("Empty output from OpenAI API")
            return json.dumps({"error": "Empty response from OpenAI", "idea1": [{"title": "Sample Title", "prompt": "Sample prompt", "caption": "Sample caption"}]})
        
        # Clean output by removing Markdown code blocks if present
        cleaned_output = output
        if output.strip().startswith('```'):
            # Extract content from the markdown code block
            lines = output.strip().split('\n')
            if len(lines) > 1:  # Skip the first line (```json)
                # Remove the first line and any trailing ```
                cleaned_output = '\n'.join(lines[1:])
                if cleaned_output.strip().endswith('```'):
                    cleaned_output = cleaned_output.strip()[:-3].strip()
            
            print("Cleaned output from markdown code block")
        
        # Try to parse the output as JSON to ensure it's valid
        try:
            parsed_json = json.loads(cleaned_output)
            print("Output is valid JSON after cleaning")
            return json.dumps(parsed_json)  # Return properly formatted JSON
        except json.JSONDecodeError as e:
            print(f"Output is not valid JSON even after cleaning: {e}")
            print("Raw output:", output)
            # Return a fallback JSON with some of the raw output
            return json.dumps({
                "error": "Invalid JSON from API", 
                "idea1": [{
                    "title": "JSON Error", 
                    "prompt": "The API response couldn't be processed correctly. We'll fix this soon!", 
                    "caption": "Please try again"
                }],
                "raw_output_sample": output[:200].replace('"', '\\"')
            })
            
        print("Trend search complete.")
        return json.dumps(parsed_json)
        
    except Exception as e:
        print(f"Error with OpenAI API call: {e}")
        # Return a fallback JSON that the frontend can handle
        return json.dumps({"error": "API Error", "idea1": [{"title": "API Error", "prompt": "There was an error calling the OpenAI API: " + str(e).replace('"', '\\"'), "caption": "Please try again"}]})

def main(brand_name, brand_desription, brand_website, product_type):
    trend_search(brand_name, brand_desription, brand_website, product_type)

if __name__ == "__main__":
    main()