import os
from flask import Blueprint, jsonify, request
from database.repositories.fileRepository import getAllFiles, createFile, getFileById, updateFile, removeFile
from utilities.utils import serializeList
from jsonschema import validate
from services.fileService import saveFile, renameFile, deleteFile
from services.gcodeService import validateGcodeFile

fileBlueprint = Blueprint('fileBlueprint', __name__)

CREATE_FILE_SCHEMA = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string', 'pattern': '^[1-9]\d*$'},
    },
    'required': ['user_id'],
}

UPDATE_FILE_SCHEMA = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'file_name': {'type': 'string'},
    },
    'required': ['user_id', 'file_name'],
}

@fileBlueprint.route('/', methods=['GET'])
@fileBlueprint.route('/all', methods=['GET'])
def getFiles():
    # TODO: Get user ID from authorization header
    user_id = 1
    files = serializeList(getAllFiles(user_id))
    return jsonify(files)

@fileBlueprint.route('/', methods=['POST'])
def uploadFile():
    try:
        validate(instance=request.form, schema=CREATE_FILE_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400
    # Check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return {'response': 'ERROR: No file part'}, 400
    file = request.files['file']
    # Check if the user did actually select a file
    if not file or file.filename == '':
        print('No selected file')
        return {'response': 'ERROR: No selected file'}, 400

    userId = request.form['user_id']

    # Validate the file content prior to save it
    try:
        validateGcodeFile(file)
    except Exception as error:
        return {'Error': str(error)}, 400

    # Save file in the file system
    try:
        generatedFilename = saveFile(userId, file)
    except Exception as error:
        return {'Error': str(error)}, 400

    # Create an entry for the file in the DB
    try:
        createFile(userId, file.filename, generatedFilename)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'response': 'OK'}, 200

@fileBlueprint.route('/<int:file_id>', methods=['PUT'])
def updateFileName(file_id):
    try:
        validate(instance=request.json, schema=UPDATE_FILE_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    userId = request.json['user_id']
    newFileName = request.json['file_name']

    # Update file in the file system
    try:
        file = getFileById(file_id)
        generatedFilename = renameFile(file.file_path, userId, newFileName)
    except Exception as error:
        return {'Error': str(error)}, 400

    # Update the entry for the file in the DB
    try:
        updateFile(file_id, userId, newFileName, generatedFilename)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'response': 'OK'}, 200

@fileBlueprint.route('/<int:file_id>', methods=['DELETE'])
def removeExistingUser(file_id):
    # Remove the file from the file system
    try:
        file = getFileById(file_id)
        deleteFile(file.file_path)
    except Exception as error:
        return {'Error': str(error)}, 400

    # Remove the entry for the file in the DB
    try:
        removeFile(file_id)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The file was successfully removed'}, 200
