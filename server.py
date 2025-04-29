from flask import Flask, send_file, request, jsonify # type: ignore
import webSearch
import traceback
import json

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('TrendlyAI.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=5000) 