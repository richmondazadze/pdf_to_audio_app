from celery import Celery
from gtts import gTTS
import os
from utils import extract_text_from_pdf
from config import Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
celery.conf.update(result_backend=Config.CELERY_RESULT_BACKEND)

@celery.task(bind=True)
def convert_pdf_to_audio(self, pdf_path):
    try:
        text = extract_text_from_pdf(pdf_path)
        tts = gTTS(text)
        audio_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.mp3'
        audio_path = os.path.join(Config.UPLOAD_FOLDER, audio_filename)
        tts.save(audio_path)
        return {'result': audio_filename}
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
        raise
