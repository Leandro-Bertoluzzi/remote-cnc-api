from flask import Blueprint, jsonify, request
from jsonschema import validate

from authMiddleware import token_required, only_admin
from core.database.repositories.fileRepository import FileRepository
from utilities.utils import serializeList
from core.utils.files import saveFile, renameFile, deleteFile, saveFileToFS
from services.gcodeService import validateGcodeFile

fileBlueprint = Blueprint('fileBlueprint', __name__)

UPDATE_FILE_SCHEMA = {
    'type': 'object',
    'properties': {
        'file_name': {'type': 'string'},
    },
    'required': ['file_name'],
}

@fileBlueprint.route('/', methods=['GET'])
@token_required
def getFiles(user):
    repository = FileRepository()
    files = serializeList(repository.get_all_files_from_user(user.id))
    return jsonify(files)

@fileBlueprint.route('/all', methods=['GET'])
@token_required
@only_admin
def getFilesFromAllUsers(admin):
    repository = FileRepository()
    files = serializeList(repository.get_all_files())
    return jsonify(files)

@fileBlueprint.route('/', methods=['POST'])
@token_required
def uploadFile(user):
    # Check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return {'error': 'ERROR: No file part'}, 400
    file = request.files['file']
    # Check if the user did actually select a file
    if not file or file.filename == '':
        print('No selected file')
        return {'error': 'ERROR: No selected file'}, 400

    # Validate the file content prior to save it
    try:
        validateGcodeFile(file)
    except Exception as error:
        return {'error': str(error)}, 400

    # Save file in the file system
    try:
        generatedFilename = saveFile(user.id, file)
    except Exception as error:
        return {'error': str(error)}, 400

    # Create an entry for the file in the DB
    try:
        repository = FileRepository()
        repository.create_file(user.id, file.filename, generatedFilename)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'response': 'OK'}, 200

@fileBlueprint.route('/<int:file_id>', methods=['PUT'])
@token_required
def updateFileName(user, file_id):
    try:
        validate(instance=request.json, schema=UPDATE_FILE_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    newFileName = request.json['file_name']

    # Update file in the file system
    try:
        repository = FileRepository()
        file = repository.get_file_by_id(file_id)
        generatedFilename = renameFile(file.file_path, user.id, newFileName)
    except Exception as error:
        return {'error': str(error)}, 400

    # Update the entry for the file in the DB
    try:
        repository = FileRepository()
        repository.update_file(user.id, file_id, newFileName, generatedFilename)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'response': 'OK'}, 200

@fileBlueprint.route('/<int:file_id>', methods=['DELETE'])
def removeExistingFile(file_id):
    # Remove the file from the file system
    try:
        repository = FileRepository()
        file = repository.get_file_by_id(file_id)
        deleteFile(file.file_path)
    except Exception as error:
        return {'error': str(error)}, 400

    # Remove the entry for the file in the DB
    try:
        repository = FileRepository()
        repository.remove_file(file_id)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The file was successfully removed'}, 200

###################################################################################

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

fileRoutes = APIRouter()

class FileUpdateModel(BaseModel):
    file_name: str

@fileRoutes.get('/files/')
def get_files():
    repository = FileRepository()
    files = serializeList(repository.get_all_files_from_user(1))
    return files

@fileRoutes.get('/files/all')
def get_files_from_all_users():
    repository = FileRepository()
    files = serializeList(repository.get_all_files())
    return files

@fileRoutes.post('/files/')
def upload_file(file: UploadFile):
    # Validate the file content prior to save it
    try:
        validateGcodeFile(file.file)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Save file in the file system
    try:
        generatedFilename = saveFileToFS(1, file.file, file.filename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Create an entry for the file in the DB
    try:
        repository = FileRepository()
        repository.create_file(1, file.filename, generatedFilename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'response': 'OK'}

@fileRoutes.put('/files/{file_id}')
def update_file_name(file_id: int, request: FileUpdateModel):
    newFileName = request.file_name

    # Update file in the file system
    try:
        repository = FileRepository()
        file = repository.get_file_by_id(file_id)
        generatedFilename = renameFile(1, file.file_path, newFileName)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Update the entry for the file in the DB
    try:
        repository = FileRepository()
        repository.update_file(file_id, 1, newFileName, generatedFilename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'response': 'OK'}

@fileRoutes.delete('/files/{file_id}')
def remove_existing_file(file_id: int):
    # Remove the file from the file system
    try:
        repository = FileRepository()
        file = repository.get_file_by_id(file_id)
        deleteFile(1, file.file_path)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Remove the entry for the file in the DB
    try:
        repository = FileRepository()
        repository.remove_file(file_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file was successfully removed'}
