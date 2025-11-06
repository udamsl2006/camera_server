from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "Camera Uploader Server is active!"
    })

# --- Upload route ---
@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if file part exists
    if "file" not in request.files:
        return jsonify({"error": "No file field found"}), 400

    file = request.files["file"]

    # Check if filename is valid
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Give each file a unique name (timestamp)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save the uploaded image
    file.save(filepath)

    print(f"✅ File received: {filename}")

    return jsonify({"message": "File uploaded successfully", "file": filename}), 200


# --- List all images ---
@app.route("/images", methods=["GET"])
def list_images():
    files = os.listdir(UPLOAD_FOLDER)
    files = sorted(files, reverse=True)
    return jsonify(files)


# --- Serve individual image files ---
@app.route("/images/<filename>", methods=["GET"])
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
