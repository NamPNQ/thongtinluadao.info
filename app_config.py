# -*- coding: utf-8 -*-
"""
    app_config
    ~~~~~~~~~~

    TTLD app config
"""

import os

DEBUG = True if os.getenv('ENV_STAGE', 'dev') in ['dev'] else False
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '455659619641-0cv8294sarb8ljk1sj9ada6ftdn1diei.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'q9XMbmb_B7BAtpDxyQnWVyMK')
SECRET_KEY = os.getenv('SECRET_KEY', 'staging sample key')
