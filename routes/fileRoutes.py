from authMiddleware import GetAdminDep, GetUserDep
from core.database.repositories.fileRepository import FileRepository
from core.utils.files import saveFile, renameFile, deleteFile
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from services.gcode import validateGcodeFile
from services.utilities import serializeList

fileRoutes = APIRouter(prefix="/files", tags=["Files"])


class FileUpdateModel(BaseModel):
    file_name: str


@fileRoutes.get('/')
def get_files(user: GetUserDep):
    repository = FileRepository()
    files = serializeList(repository.get_all_files_from_user(user.id))
    return files


@fileRoutes.get('/all')
def get_files_from_all_users(admin: GetAdminDep):
    repository = FileRepository()
    files = serializeList(repository.get_all_files())
    return files


@fileRoutes.post('/')
def upload_file(file: UploadFile, user: GetUserDep):
    # Validate the file content prior to save it
    try:
        validateGcodeFile(file.file)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Save file in the file system
    try:
        generatedFilename = saveFile(user.id, file.file, file.filename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Create an entry for the file in the DB
    try:
        repository = FileRepository()
        repository.create_file(user.id, file.filename, generatedFilename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'response': 'OK'}


@fileRoutes.put('/{file_id}')
def update_file_name(
    file_id: int,
    request: FileUpdateModel,
    user: GetUserDep
):
    newFileName = request.file_name

    # Update file in the file system
    try:
        repository = FileRepository()
        file = repository.get_file_by_id(file_id)
        generatedFilename = renameFile(user.id, file.file_path, newFileName)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Update the entry for the file in the DB
    try:
        repository = FileRepository()
        repository.update_file(file_id, user.id, newFileName, generatedFilename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'response': 'OK'}


@fileRoutes.delete('/{file_id}')
def remove_existing_file(file_id: int, user: GetUserDep):
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
