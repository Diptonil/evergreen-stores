import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
REDIS_SENTINEL = os.getenv('REDIS_SENTINEL')
REDIS_MASTER_NAME = os.getenv('REDIS_MASTER_NAME')
