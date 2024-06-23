from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import pyttsx3
import os
from PyPDF2 import PdfFileReader

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def pdf_to_audio(pdf_path, audio_path):
    reader = PdfFileReader(open(pdf_path, 'rb'))
    engine = pyttsx3.init()
    text = ""
    for page_num in range(reader.numPages):
        text += reader.getPage(page_num).extract_text()
    engine.save_to_file(text, audio_path)
    engine.runAndWait()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.pdf', '.mp3'))
        file.save(pdf_path)
        pdf_to_audio(pdf_path, audio_path)
        return jsonify({"audio_url": f"/download/{filename.replace('.pdf', '.mp3')}"})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
