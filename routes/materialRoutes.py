from authMiddleware import GetAdminDep
from core.database.repositories.materialRepository import MaterialRepository
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utilities.utils import serializeList

materialRoutes = APIRouter()

class MaterialRequestModel(BaseModel):
    name: str
    description: str

@materialRoutes.get('/materials/')
@materialRoutes.get('/materials/all')
def get_materials(admin: GetAdminDep):
    repository = MaterialRepository()
    materials = serializeList(repository.get_all_materials())
    return materials

@materialRoutes.post('/materials/')
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

@materialRoutes.put('/materials/{material_id}')
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

@materialRoutes.delete('/materials/{material_id}')
def remove_material(material_id: int, admin: GetAdminDep):
    try:
        repository = MaterialRepository()
        repository.remove_material(material_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The material was successfully removed'}
