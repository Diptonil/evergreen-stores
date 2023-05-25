import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
MOVIE_DATABASE_USERNAME = os.getenv('MOVIE_DATABASE_USERNAME')
MOVIE_DATABASE_PASSWORD = os.getenv('MOVIE_DATABASE_PASSWORD')
MOVIE_DATABASE_URL = os.getenv('MOVIE_DATABASE_URL')

print(SECRET_KEY)
