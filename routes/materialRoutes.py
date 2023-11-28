from authMiddleware import GetAdminDep, GetUserDep
from core.database.repositories.materialRepository import MaterialRepository
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utilities.utils import serializeList

materialRoutes = APIRouter(prefix="/materials", tags=["Materials"])


class MaterialRequestModel(BaseModel):
    name: str
    description: str


@materialRoutes.get('/')
@materialRoutes.get('/all')
def get_materials(user: GetUserDep):
    repository = MaterialRepository()
    materials = serializeList(repository.get_all_materials())
    return materials


@materialRoutes.post('/')
def create_material(request: MaterialRequestModel, admin: GetAdminDep):
    # Get data from request body
    materialName = request.name
    materialDescription = request.description

    try:
        repository = MaterialRepository()
        repository.create_material(materialName, materialDescription)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The material was successfully created'}


@materialRoutes.put('/{material_id}')
def update_material(
    request: MaterialRequestModel,
    material_id: int,
    admin: GetAdminDep
):
    materialName = request.name
    materialDescription = request.description

    try:
        repository = MaterialRepository()
        repository.update_material(material_id, materialName, materialDescription)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The material was successfully updated'}


@materialRoutes.delete('/{material_id}')
def remove_material(material_id: int, admin: GetAdminDep):
    try:
        repository = MaterialRepository()
        repository.remove_material(material_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The material was successfully removed'}
