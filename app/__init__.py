from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from celery import Celery

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')
    
    CORS(app)
    CSRFProtect(app)
    
    from .views import main
    app.register_blueprint(main)

    init_celery(app)
    
    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

def init_celery(app):
    celery = make_celery(app)
    celery.conf.update(app.config)
    app.celery = celery
