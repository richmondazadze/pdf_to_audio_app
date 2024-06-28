import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'your-secret-key'
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
DOWNLOAD_FOLDER = os.path.join(basedir, 'downloads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
