from flask import Blueprint, jsonify, request
from jsonschema import validate

from authMiddleware import token_required, only_admin
from database.repositories.materialRepository import getAllMaterials, createMaterial, updateMaterial, removeMaterial
from utilities.utils import serializeList

materialBlueprint = Blueprint('materialBlueprint', __name__)

MATERIAL_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': ['name', 'description'],
}

@materialBlueprint.route('/', methods=['GET'])
@materialBlueprint.route('/all', methods=['GET'])
@token_required
@only_admin
def getMaterials(admin):
    materials = serializeList(getAllMaterials())
    return jsonify(materials)

@materialBlueprint.route('/', methods=['POST'])
@token_required
@only_admin
def createNewMaterial(admin):
    try:
        validate(instance=request.json, schema=MATERIAL_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    materialName = request.json['name']
    materialDescription = request.json['description']

    try:
        createMaterial(materialName, materialDescription)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The material was successfully created'}, 200

@materialBlueprint.route('/<int:material_id>', methods=['PUT'])
@token_required
@only_admin
def updateExistingMaterial(admin, material_id):
    try:
        validate(instance=request.json, schema=MATERIAL_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    materialName = request.json['name']
    materialDescription = request.json['description']

    try:
        updateMaterial(material_id, materialName, materialDescription)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The material was successfully updated'}, 200

@materialBlueprint.route('/<int:material_id>', methods=['DELETE'])
@token_required
@only_admin
def removeExistingMaterial(admin, material_id):
    try:
        removeMaterial(material_id)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The material was successfully removed'}, 200
