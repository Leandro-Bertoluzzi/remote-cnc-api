from dotenv import load_dotenv
import os

# Take environment variables from .env.
load_dotenv()

# Get environment variables
dbPort = os.environ.get('DB_PORT')
dbUser = os.environ.get('DB_USER')
dbPass = os.environ.get('DB_PASS')
dbName = os.environ.get('DB_NAME')
FILES_FOLDER_PATH = './' + os.environ.get('FILES_FOLDER')

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{dbUser}:{dbPass}@localhost:{dbPort}/{dbName}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False