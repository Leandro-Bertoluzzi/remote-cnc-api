import os
import time
from werkzeug.utils import secure_filename
from config import FILES_FOLDER_PATH

ALLOWED_FILE_EXTENSIONS = {'txt', 'gcode'}

def allowed_file(filename):
    """Checks if the file extension is a valid one"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

def create_file_name(filename):
    """Defines a secure filename to avoid repeated files"""
    secureFilename = secure_filename(filename)
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    file_base_name = os.path.splitext(secureFilename)[0]
    file_extension = os.path.splitext(secureFilename)[1].lower()
    return f'{file_base_name}_{timestamp}{file_extension}'

def saveFile(userId, file):
    # Check if the file format is a valid one
    if not allowed_file(file.filename):
        print('Invalid file format')
        raise Exception(f'Invalid file format, must be one of: {ALLOWED_FILE_EXTENSIONS}')

    try:
        # If the folder FILES_FOLDER_PATH is not present, then create it
        if not os.path.exists(FILES_FOLDER_PATH):
            os.makedirs(FILES_FOLDER_PATH)
        
        # If the folder for the current user is not present, then create it
        user_files_folder_path = f'{FILES_FOLDER_PATH}/{userId}'
        if not os.path.exists(user_files_folder_path):
            os.makedirs(user_files_folder_path)
        
        # Save the file
        filename = create_file_name(file.filename)
        file.save(os.path.join(user_files_folder_path, filename))
    except Exception as error:
        raise Exception('There was an error writing the file in the file system')
    
    return filename

def renameFile(filePath, userId, newFileName):
    # Check if the file format is a valid one
    if not allowed_file(newFileName):
        print('Invalid file format')
        raise Exception(f'Invalid file format, must be one of: {ALLOWED_FILE_EXTENSIONS}')

    try:
        # Rename the file
        current_file_path = f'{FILES_FOLDER_PATH}/{filePath}'
        filename = create_file_name(newFileName)
        new_file_path = f'{FILES_FOLDER_PATH}/{userId}/{filename}'
        os.rename(current_file_path, new_file_path)
    except Exception as error:
        raise Exception('There was an error writing the file in the file system')
    
    return filename

def deleteFile(filePath):
    try:
        # Remove the file
        file_whole_path = f'{FILES_FOLDER_PATH}/{filePath}'
        os.remove(file_whole_path)
    except Exception as error:
        raise Exception('There was an error removing the file from the file system')