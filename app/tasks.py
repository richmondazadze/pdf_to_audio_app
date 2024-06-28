from celery import current_app as celery
from gtts import gTTS
import os
import pdfplumber
import time

@celery.task(bind=True)
def convert_pdf_to_audio(self, file_path):
    try:
        self.update_state(state='PROGRESS', meta={'status': 'Extracting text from PDF...'})
        text = extract_text_from_pdf(file_path)
        
        self.update_state(state='PROGRESS', meta={'status': 'Converting text to audio...'})
        tts = gTTS(text)
        audio_path = file_path.replace('.pdf', '.mp3')
        tts.save(audio_path)
        
        self.update_state(state='PROGRESS', meta={'status': 'Saving audio file...'})
        os.rename(audio_path, os.path.join('downloads', os.path.basename(audio_path)))
        
        return {'status': 'Task completed!', 'result': os.path.basename(audio_path)}
    except Exception as e:
        return {'status': 'Task failed', 'result': str(e)}

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text
