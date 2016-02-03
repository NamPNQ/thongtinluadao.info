# -*- coding: utf-8 -*-
"""
    app_config
    ~~~~~~~~~~

    TTLD app config
"""

import os

DEBUG = True if os.getenv('ENV_STAGE', 'dev') in ['dev'] else False
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '513593066071-r10fps7htf4fvuvunad08p065rsbe6h9.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'dtAIGo1CZkw8Ibuk1jlGpK5G')
SECRET_KEY = os.getenv('SECRET_KEY', 'staging sample key')

