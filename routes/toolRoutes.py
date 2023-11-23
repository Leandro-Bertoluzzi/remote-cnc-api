from flask import Blueprint, jsonify, request
from jsonschema import validate

from authMiddleware import token_required, only_admin
from core.database.repositories.toolRepository import ToolRepository
from utilities.utils import serializeList

toolBlueprint = Blueprint('toolBlueprint', __name__)

TOOL_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': ['name', 'description'],
}

@toolBlueprint.route('/', methods=['GET'])
@toolBlueprint.route('/all', methods=['GET'])
@token_required
@only_admin
def getTools(admin):
    repository = ToolRepository()
    tools = serializeList(repository.get_all_tools())
    return jsonify(tools)

@toolBlueprint.route('/', methods=['POST'])
@token_required
@only_admin
def createNewTool(admin):
    try:
        validate(instance=request.json, schema=TOOL_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    toolName = request.json['name']
    toolDescription = request.json['description']

    try:
        repository = ToolRepository()
        repository.create_tool(toolName, toolDescription)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The tool was successfully created'}, 200

@toolBlueprint.route('/<int:tool_id>', methods=['PUT'])
@token_required
@only_admin
def updateExistingTool(admin, tool_id):
    try:
        validate(instance=request.json, schema=TOOL_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    toolName = request.json['name']
    toolDescription = request.json['description']

    try:
        repository = ToolRepository()
        repository.update_tool(tool_id, toolName, toolDescription)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The tool was successfully updated'}, 200

@toolBlueprint.route('/<int:tool_id>', methods=['DELETE'])
@token_required
@only_admin
def removeExistingTool(admin, tool_id):
    try:
        repository = ToolRepository()
        repository.remove_tool(tool_id)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The tool was successfully removed'}, 200
