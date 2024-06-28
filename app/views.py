from flask import Blueprint, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from .tasks import convert_pdf_to_audio
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        task = convert_pdf_to_audio.apply_async(args=[file_path])
        return jsonify(task_id=task.id), 202
    return jsonify(error='Invalid file format'), 400

@main.route('/status/<task_id>')
def task_status(task_id):
    task = convert_pdf_to_audio.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    return jsonify(response)

@main.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('downloads', filename), as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}
