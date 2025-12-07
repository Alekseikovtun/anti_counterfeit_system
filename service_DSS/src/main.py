from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/status", methods=["GET"])
def status_check():
    return jsonify({"status": "ok"})

@app.route("/upload_files_to_storage", methods=["POST"])
def upload_files():
    app.config['UPLOAD_FOLDER'] = 'D:/_project/anti_counterfeit_system/service_DSS/storage'
    
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    files = request.files.getlist('files')

    if len(files) == 0:
        return jsonify({"error": "No selected file"}), 400
    
    saved_files = []

    for file in files:
        if file.filename == '':
            continue
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            saved_files.append(filename)
        else:
            return jsonify({"error": f"File type not allowed: {file.filename}"}), 400

    return jsonify({"message": "File added successfully"}), 200

@app.route("/get_file/<path:filename>", methods=["GET"]) #one file
def get_file(filename):
    app.config['UPLOAD_FOLDER'] = 'D:/_project/anti_counterfeit_system/service_DSS/storage'
    
    safe_name = secure_filename(filename)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

    print(file_path)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], safe_name, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)