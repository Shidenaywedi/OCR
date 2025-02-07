from flask import Flask, jsonify, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ensure that the "uploads" folder exists (it’s where you will store uploaded files)
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify(message="Hello from Flask API!")

# Example route to handle OCR requests
@app.route("/ocr", methods=["POST"])
def ocr():
    # Assuming the image is sent in the POST request
    if 'image' not in request.files:
        return jsonify(error="No image provided"), 400
    
    image_file = request.files['image']
    
    # Here you can process the image (e.g., perform OCR) – this is just a placeholder
    # You can replace it with actual OCR processing logic
    image_filename = image_file.filename
    image_file.save(os.path.join('uploads', image_filename))  # Save the uploaded file

    return jsonify(message=f"Image {image_filename} received and processed.")

# Example route to fetch some OCR results (mock)
@app.route("/result", methods=["GET"])
def result():
    # This would typically fetch results from OCR processing
    return jsonify(result="Sample OCR text from image")

if __name__ == "__main__":
    # Vercel requires the app to run on host 0.0.0.0 and port 8080
    app.run(host="0.0.0.0", port=8080)
