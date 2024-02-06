from authMiddleware import GetAdminDep, GetUserDep
from core.database.repositories.fileRepository import FileRepository, \
    DuplicatedFileError, DuplicatedFileNameError
from core.utils.files import computeSHA256FromFile, deleteFile, renameFile, saveFile
import datetime
from dbMiddleware import GetDbSession
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel, Field
from services.gcode import validateGcodeFile
from services.utilities import serializeList

fileRoutes = APIRouter(prefix="/files", tags=["Files"])


class FileUpdateModel(BaseModel):
    file_name: str


class FileResponseModel(BaseModel):
    id: int
    name: str = Field(alias="file_name")
    created_at: datetime.datetime
    user_id: int

    class Config:
        allow_population_by_field_name = True


@fileRoutes.get('', response_model_by_alias=False)
@fileRoutes.get('/', response_model_by_alias=False)
def get_files(
    user: GetUserDep,
    db_session: GetDbSession
) -> list[FileResponseModel]:
    repository = FileRepository(db_session)
    files = serializeList(repository.get_all_files_from_user(user.id))
    return files


@fileRoutes.get('/all', response_model_by_alias=False)
def get_files_from_all_users(
    admin: GetAdminDep,
    db_session: GetDbSession
) -> list[FileResponseModel]:
    repository = FileRepository(db_session)
    files = serializeList(repository.get_all_files())
    return files


@fileRoutes.post('')
@fileRoutes.post('/')
def upload_file(
    file: UploadFile,
    user: GetUserDep,
    db_session: GetDbSession
):
    repository = FileRepository(db_session)

    # Checks if the file is repeated
    file_hash = computeSHA256FromFile(file.file)
    try:
        repository.check_file_exists(user.id, file.filename, file_hash)
    except DuplicatedFileNameError:
        raise HTTPException(
            400,
            detail=f'Ya existe un archivo con el nombre <<{file.filename}>>, pruebe renombrarlo'
        )
    except DuplicatedFileError as error:
        raise HTTPException(400, detail=str(error))
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Validate the file content prior to save it
    try:
        validateGcodeFile(file.file)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Save file in the file system
    try:
        saveFile(user.id, file.file, file.filename)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Create an entry for the file in the DB
    try:
        repository.create_file(user.id, file.filename, file_hash)
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
        renameFile(user.id, file.file_name, newFileName)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Update the entry for the file in the DB
    try:
        repository.update_file(file_id, user.id, newFileName)
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
        deleteFile(1, file.file_name)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    # Remove the entry for the file in the DB
    try:
        repository.remove_file(file_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file was successfully removed'}
