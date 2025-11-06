from flask import Flask, request, send_from_directory, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# ✅ Save uploads to /app/uploads (Railway safe path)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return "No image part", 400

    image = request.files["image"]
    if image.filename == "":
        return "No selected file", 400

    # ✅ Save file with timestamp
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(save_path)
    print(f"✅ Saved: {save_path}")
    return "Uploaded", 200

@app.route("/uploads/<path:filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/images")
def list_images():
    files = sorted(os.listdir(UPLOAD_FOLDER))
    return jsonify(files)

@app.route("/")
def gallery():
    files = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    html = "<h2>Uploaded Images</h2>"
    for f in files:
        html += f'<div style="margin:10px;display:inline-block;">'
        html += f'<img src="/uploads/{f}" width="200"><br>{f}</div>'
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
