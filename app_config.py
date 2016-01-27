import os

DEBUG = True if os.getenv('ENV_STAGE', 'dev') in ['dev'] else False
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
