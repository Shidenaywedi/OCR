import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app, resources={r"/ocr": {"origins": "*"}})

OCR_SPACE_API_KEY = "your_api_key_here"  # Replace with your real API key
@app.route("/", methods=["GET"])
def say_hello():
    return jsonify(answer="hello")
@app.route("/ocr", methods=["POST"])
def ocr():
    """Handles image upload and OCR processing using OCR.Space API."""
    if 'image' not in request.files:
        return jsonify(error="No image file provided"), 400

    image_file = request.files['image']
    
    if image_file.filename == '':
        return jsonify(error="No selected file"), 400

    # Convert image to base64
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Send image to OCR.Space API
    response = requests.post(
        "https://api.ocr.space/parse/image",
        data={
            "apikey": OCR_SPACE_API_KEY,
            "language": "tir",  # Tigrinya language code
            "isOverlayRequired": False,
            "base64Image": f"data:image/jpeg;base64,{image_base64}",
        },
    )

    # Process response
    result = response.json()
    if result.get("ParsedResults"):
        extracted_text = result["ParsedResults"][0].get("ParsedText", "").strip()
        return jsonify(text=extracted_text)
    else:
        return jsonify(error="OCR failed"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
