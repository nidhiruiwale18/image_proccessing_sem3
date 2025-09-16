from flask import Flask, request, jsonify
import os
import cv2
from PIL import Image

app = Flask(_name_)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Astronomical Image Processing Backend is Running 🚀"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Example: simple grayscale processing
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    output_path = os.path.join(OUTPUT_FOLDER, f"processed_{file.filename}")
    cv2.imwrite(output_path, gray)

    return jsonify({
        "message": "File processed successfully",
        "processed_image_url": f"/{output_path}"
    })

if _name_ == "_main_":
    app.run(debug=True, host="0.0.0.0")
