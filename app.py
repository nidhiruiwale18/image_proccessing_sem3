from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import torch
from model import ReconModel
from utils import run_cs_reconstruction

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app = Flask(_name_)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Load trained model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = ReconModel().to(device)
model.load_state_dict(torch.load("checkpoint.pth", map_location=device))
model.eval()

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Run reconstruction pipeline
    recon_path = os.path.join(app.config['OUTPUT_FOLDER'], "recon_" + filename)
    run_cs_reconstruction(filepath, recon_path, model, device)

    return jsonify({"result": recon_path})

@app.route("/results/<filename>")
def get_result(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if _name_ == "_main_":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
