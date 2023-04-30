import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from config import FILES_FOLDER_PATH

fileBlueprint = Blueprint('fileBlueprint', __name__)

ALLOWED_FILE_EXTENSIONS = {'txt', 'gcode'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

@fileBlueprint.route('/', methods=['POST'])
def uploadFile():
    # Check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return {'response': 'ERROR: No file part'}, 400
    file = request.files['file']
    # Check if the user did actually select a file
    if not file or file.filename == '':
        print('No selected file')
        return {'response': 'ERROR: No selected file'}, 400
    # Check if the file format is a valid one
    if not allowed_file(file.filename):
        print('Invalid file format')
        return {'response': 'ERROR: Invalid file format'}, 400
    # Saves the file in the file system
    filename = secure_filename(file.filename)
    # If the folder FILES_FOLDER_PATH is not present, then create it.
    if not os.path.exists(FILES_FOLDER_PATH):
        os.makedirs(FILES_FOLDER_PATH)
    file.save(os.path.join(FILES_FOLDER_PATH, filename))
    return {'response': 'OK'}, 200