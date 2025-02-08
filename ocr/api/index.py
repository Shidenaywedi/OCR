from flask import Flask, jsonify, request
import pytesseract
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/ocr": {"origins": "*"}})  # Allow requests from all origins


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'}

def allowed_file(filename):
    """Check if the file has a valid image extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def home():
    return jsonify(message="Hello from Flask OCR API! 😊")

@app.route("/ocr", methods=["POST"])
def ocr():
    """Handles image upload and OCR processing with Tigrinya language support."""
    if 'image' not in request.files:
        return jsonify(error="No image file provided"), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify(error="No selected file"), 400

    if not allowed_file(image_file.filename):
        return jsonify(error="Invalid file type. Allowed types: png, jpg, jpeg, tiff, bmp, gif"), 400

    try:
        # Read image directly from memory
        image = Image.open(io.BytesIO(image_file.read()))

        # Perform OCR using Tesseract with Tigrinya language
        extracted_text = pytesseract.image_to_string(image, lang="tir")

        return jsonify(text=extracted_text.strip())  # Return extracted text
    except Exception as e:
        return jsonify(error=f"An error occurred: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
