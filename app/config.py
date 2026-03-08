# app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    BABEL_DEFAULT_LOCALE = 'es'
    BABEL_SUPPORTED_LOCALES = ['es', 'en']
    ORION_BASE_URL = os.environ.get('ORION_BASE_URL', 'http://localhost:1026')
    AUTO_BOOTSTRAP = os.environ.get('AUTO_BOOTSTRAP', 'true').lower() == 'true'