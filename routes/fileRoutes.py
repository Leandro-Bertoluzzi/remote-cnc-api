from authMiddleware import GetAdminDep, GetUserDep
from core.database.repositories.fileRepository import FileRepository
from core.utils.files import saveFile, renameFile, deleteFile
from dbMiddleware import GetDbSession
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from services.gcode import validateGcodeFile
from services.utilities import serializeList

fileRoutes = APIRouter(prefix="/files", tags=["Files"])


class FileUpdateModel(BaseModel):
    file_name: str


class FileResponseModel(BaseModel):
    file_name: str
    user_id: int


@fileRoutes.get('/')
def get_files(
    user: GetUserDep,
    db_session: GetDbSession
) -> list[FileResponseModel]:
    repository = FileRepository(db_session)
    files = serializeList(repository.get_all_files_from_user(user.id))
    return files


@fileRoutes.get('/all')
def get_files_from_all_users(
    admin: GetAdminDep,
    db_session: GetDbSession
) -> list[FileResponseModel]:
    repository = FileRepository(db_session)
    files = serializeList(repository.get_all_files())
    return files


@fileRoutes.post('/')
def upload_file(
    file: UploadFile,
    user: GetUserDep,
    db_session: GetDbSession
):
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
        repository = FileRepository(db_session)
        repository.create_file(user.id, file.filename, generatedFilename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file was successfully uploaded'}


@fileRoutes.put('/{file_id}')
def update_file_name(
    file_id: int,
    request: FileUpdateModel,
    user: GetUserDep,
    db_session: GetDbSession
):
    newFileName = request.file_name

    # Update file in the file system
    repository = FileRepository(db_session)
    try:
        file = repository.get_file_by_id(file_id)
        generatedFilename = renameFile(user.id, file.file_path, newFileName)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Update the entry for the file in the DB
    try:
        repository.update_file(file_id, user.id, newFileName, generatedFilename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file name was successfully updated'}


@fileRoutes.delete('/{file_id}')
def remove_existing_file(
    file_id: int,
    user: GetUserDep,
    db_session: GetDbSession
):
    # Remove the file from the file system
    repository = FileRepository(db_session)
    try:
        file = repository.get_file_by_id(file_id)
        deleteFile(1, file.file_path)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Remove the entry for the file in the DB
    try:
        repository.remove_file(file_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file was successfully removed'}
