from flask import Blueprint, jsonify, request
from database.repositories.taskRepository import getAllTasks, createTask, \
    updateTask, removeTask, getTasksByStatus, updateTaskStatus
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
        'priority': {'type': 'integer'},
        'note': {'type': 'string'},
    },
    'required': ['user_id'],
}

UPDATE_TASK_STATUS_SCHEMA = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string', 'enum': VALID_STATUSES},
        'admin_id': {'type': 'integer'},
        'cancellation_reason': {'type': 'string'},
    },
    'required': ['status'],
}

GET_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string', 'enum': VALID_STATUSES},
    },
}

@taskBlueprint.route('/', methods=['GET'])
def getTasks():
    try:
        validate(instance=request.args, schema=GET_TASK_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    status = request.args.get('status')
    # TODO: Get user ID from authorization header
    user_id = 1

    if not status or status == 'all':
        tasks = serializeList(getAllTasks(user_id))
        return jsonify(tasks)

    tasks = serializeList(getTasksByStatus(user_id, status))
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

@taskBlueprint.route('/<int:task_id>/status', methods=['PUT'])
def updateExistingTaskStatus(task_id):
    try:
        validate(instance=request.json, schema=UPDATE_TASK_STATUS_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    jsonData = request.json
    taskStatus = jsonData.get('status')
    admin_id = jsonData.get('admin_id')
    cancellation_reason = jsonData.get('cancellation_reason')

    try:
        updateTaskStatus(
            task_id,
            taskStatus,
            admin_id,
            cancellation_reason
        )
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The task status was successfully updated'}, 200

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
    taskPriority = jsonData.get('priority')

    print("User ID: ", userId)

    try:
        updateTask(
            task_id,
            userId,
            fileId,
            toolId,
            materialId,
            taskName,
            taskNote,
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
