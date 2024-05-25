from authMiddleware import GetAdminDep, GetUserDep
from config import PROJECT_ROOT
from core.database.repositories.fileRepository import FileRepository
from core.utils.fileManager import FileManager
import datetime
from dbMiddleware import GetDbSession
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel, Field
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
    user: GetUserDep
):
    file_manager = FileManager(PROJECT_ROOT)
    try:
        file_manager.upload_file(user.id, file.filename, file.file)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file was successfully uploaded'}


@fileRoutes.put('/{file_id}')
def update_file_name(
    file_id: int,
    request: FileUpdateModel,
    user: GetUserDep
):
    file_manager = FileManager(PROJECT_ROOT)
    try:
        file_manager.rename_file_by_id(user.id, file_id, request.file_name)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file name was successfully updated'}


@fileRoutes.delete('/{file_id}')
def remove_existing_file(
    file_id: int,
    user: GetUserDep
):
    file_manager = FileManager(PROJECT_ROOT)
    try:
        file_manager.remove_file_by_id(file_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The file was successfully removed'}
