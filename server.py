from flask import Flask, send_file, request, jsonify # type: ignore
import webSearch
import traceback
import json
import os
import generateImage
import base64
from werkzeug.utils import secure_filename
import Instabot

app = Flask(__name__, static_folder='.', static_url_path='')
UPLOAD_FOLDER = '/Users/rushiljhaveri/Desktop/Coding/AIAgents/TrendlyAI/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return app.send_static_file('TrendlyAI.html')

@app.route('/post_to_instagram', methods=['POST'])
def post_to_instagram_route():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        username = data.get('username')
        password = data.get('password')
        caption = data.get('caption')
        image_path = data.get('image_path', 'generated.jpeg')  # Default to the last generated image
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
            
        if not caption:
            return jsonify({"error": "Caption is required"}), 400
            
        if not os.path.exists(image_path):
            return jsonify({"error": f"Image not found at {image_path}"}), 400
            
        # Call the Instagram posting function
        success, message = Instabot.post_to_instagram(username, password, image_path, caption)
        
        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 500
            
    except Exception as e:
        print("Error posting to Instagram:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/trend_search', methods=['POST'])
def trend_search():
    # Get the request data
    data = request.json
    
    print("Received request data:", data)
    
    brand_name = data.get('brand_name', '')
    brand_description = data.get('brand_description', '')
    brand_website = data.get('brand_website', '')
    product_type = data.get('product_type', '')
    
    print(f"Processing with: Brand: {brand_name}, Product: {product_type}, Website: {brand_website}")
    
    # Call the trend_search function from webSearch.py
    try:
        result = webSearch.trend_search(brand_name, brand_description, brand_website, product_type)
        print("Raw result from webSearch:", result)
        
        # Convert result string to JSON
        try:
            json_result = json.loads(result)
            return jsonify(json_result)
        except json.JSONDecodeError as je:
            print("JSON parsing error:", str(je))
            print("Result that couldn't be parsed:", result)
            return jsonify({"error": "Invalid JSON format returned from trend search", 
                           "details": str(je),
                           "raw_output": result}), 400
                           
    except Exception as e:
        print("Exception occurred:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    try:
        # Check if files were uploaded
        if 'files' not in request.files:
            return jsonify({"error": "No files uploaded"}), 400
        
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({"error": "No files selected"}), 400
        
        # Get prompt from request
        prompt = request.form.get('prompt', '')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Save uploaded files temporarily
        image_paths = []
        for file in files:
            if file.filename == '':
                continue
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            image_paths.append(file_path)
        
        if not image_paths:
            return jsonify({"error": "No valid files uploaded"}), 400
        
        # Call the generate_image function
        print(f"Generating image with prompt: {prompt} and {len(image_paths)} images")
        
        # Pass multiple image paths to generate_image
        result = generateImage.generate_image(prompt, image_paths if len(image_paths) > 1 else image_paths[0])
        
        # Return the image data
        return jsonify({
            "success": True,
            "image_base64": result["image_base64"],
            "message": f"Image generated successfully using {len(image_paths)} branding images"
        })
        
    except Exception as e:
        print("Error generating image:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 