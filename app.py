from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from gtts import gTTS
import os
from utils import extract_text_from_pdf, allowed_file
from config import Config

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            text = extract_text_from_pdf(filepath)
            tts = gTTS(text)
            audio_filename = os.path.splitext(filename)[0] + '.mp3'
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            tts.save(audio_path)
            return jsonify(audio_file=audio_filename), 200
        except Exception as e:
            return jsonify(error=str(e)), 500
    return jsonify(error="Invalid file format"), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
