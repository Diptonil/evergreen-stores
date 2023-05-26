import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

REDIS_SENTINEL = os.getenv('REDIS_SENTINEL')
REDIS_MASTER_NAME = os.getenv('REDIS_MASTER_NAME')
REDIS_SOCKET_TIMEOUT = 0.1
REDIS_MAX_RETRIES = 3
REDIS_RETRY_BACKOFF_SECONDS = 5
