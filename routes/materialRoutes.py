from flask import Blueprint, jsonify, request
from database.repositories.materialRepository import getAllMaterials, createMaterial, updateMaterial, removeMaterial
from utilities.utils import serializeList
from jsonschema import validate

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
def getMaterials():
    materials = serializeList(getAllMaterials())
    return jsonify(materials)

@materialBlueprint.route('/', methods=['POST'])
def createNewMaterial():
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
def updateExistingMaterial(material_id):
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
def removeExistingMaterial(material_id):
    try:
        removeMaterial(material_id)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The material was successfully removed'}, 200