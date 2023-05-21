from dotenv import load_dotenv
import os

# Take environment variables from .env.
load_dotenv()

# Get environment variables
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
FILES_FOLDER_PATH = './' + os.environ.get('FILES_FOLDER')
SERIAL_PORT = os.environ.get('SERIAL_PORT')
SERIAL_BAUDRATE = os.environ.get('SERIAL_BAUDRATE')

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
