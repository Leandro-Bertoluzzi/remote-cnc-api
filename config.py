from dotenv import load_dotenv
import os

# Take environment variables from .env.
load_dotenv()

# Get environment variables
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
SERIAL_PORT = os.environ.get('SERIAL_PORT')
SERIAL_BAUDRATE = os.environ.get('SERIAL_BAUDRATE')
TOKEN_SECRET = os.environ.get('TOKEN_SECRET', '')
