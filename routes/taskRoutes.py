from flask import Blueprint, jsonify, request
from database.repositories.taskRepository import getAllTasks, createTask, updateTask, removeTask
from utilities.utils import serializeList
from database.models.task import VALID_STATUSES
from jsonschema import validate

taskBlueprint = Blueprint('taskBlueprint', __name__)

CREATE_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'file_id': {'type': 'integer'},
        'tool_id': {'type': 'integer'},
        'material_id': {'type': 'integer'},
        'name': {'type': 'string'},
        'note': {'type': 'string'},
    },
    'required': [
        'name',
        'user_id',
        'file_id',
        'tool_id',
        'material_id'
    ],
}

UPDATE_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'file_id': {'type': 'integer'},
        'tool_id': {'type': 'integer'},
        'material_id': {'type': 'integer'},
        'name': {'type': 'string'},
        'status': {'type': 'string', 'enum': VALID_STATUSES},
        'priority': {'type': 'integer'},
        'note': {'type': 'string'},
    },
}

@taskBlueprint.route('/', methods=['GET'])
@taskBlueprint.route('/all', methods=['GET'])
def getTasks():
    tasks = serializeList(getAllTasks())
    return jsonify(tasks)

@taskBlueprint.route('/', methods=['POST'])
def createNewTask():
    try:
        validate(instance=request.json, schema=CREATE_TASK_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    jsonData = request.json
    userId = jsonData.get('user_id')
    fileId = jsonData.get('file_id')
    toolId = jsonData.get('tool_id')
    materialId = jsonData.get('material_id')
    taskName = jsonData.get('name')
    taskNote = jsonData.get('note')

    try:
        createTask(
            userId,
            fileId,
            toolId,
            materialId,
            taskName,
            taskNote
        )
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The task was successfully created'}, 200

@taskBlueprint.route('/<int:task_id>', methods=['PUT'])
def updateExistingTask(task_id):
    try:
        validate(instance=request.json, schema=UPDATE_TASK_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    jsonData = request.json
    userId = jsonData.get('user_id')
    fileId = jsonData.get('file_id')
    toolId = jsonData.get('tool_id')
    materialId = jsonData.get('material_id')
    taskName = jsonData.get('name')
    taskNote = jsonData.get('note')
    taskStatus = jsonData.get('status')
    taskPriority = jsonData.get('priority')

    try:
        updateTask(
            task_id,
            userId,
            fileId,
            toolId,
            materialId,
            taskName,
            taskNote,
            taskStatus,
            taskPriority
        )
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The task was successfully updated'}, 200

@taskBlueprint.route('/<int:task_id>', methods=['DELETE'])
def removeExistingTask(task_id):
    try:
        removeTask(task_id)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The task was successfully removed'}, 200
