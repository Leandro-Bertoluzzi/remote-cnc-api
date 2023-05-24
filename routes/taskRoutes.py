from flask import Blueprint, jsonify, request
from jsonschema import validate

from authMiddleware import token_required, only_admin
from database.models.task import VALID_STATUSES
from database.repositories.taskRepository import getAllTasks, createTask, \
    updateTask, removeTask, getTasksByStatus, updateTaskStatus
from utilities.utils import serializeList

taskBlueprint = Blueprint('taskBlueprint', __name__)

CREATE_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'file_id': {'type': 'integer'},
        'tool_id': {'type': 'integer'},
        'material_id': {'type': 'integer'},
        'note': {'type': 'string'},
    },
    'required': [
        'name',
        'file_id',
        'tool_id',
        'material_id'
    ],
}

UPDATE_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'file_id': {'type': 'integer'},
        'tool_id': {'type': 'integer'},
        'material_id': {'type': 'integer'},
        'name': {'type': 'string'},
        'priority': {'type': 'integer'},
        'note': {'type': 'string'},
    },
}

UPDATE_TASK_STATUS_SCHEMA = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string', 'enum': VALID_STATUSES},
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
@token_required
def getTasks(user):
    try:
        validate(instance=request.args, schema=GET_TASK_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    status = request.args.get('status')

    if not status or status == 'all':
        tasks = serializeList(getAllTasks(user.id))
        return jsonify(tasks)

    tasks = serializeList(getTasksByStatus(user,id, status))
    return jsonify(tasks)

@taskBlueprint.route('/', methods=['POST'])
@token_required
def createNewTask(user):
    try:
        validate(instance=request.json, schema=CREATE_TASK_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    jsonData = request.json
    fileId = jsonData.get('file_id')
    toolId = jsonData.get('tool_id')
    materialId = jsonData.get('material_id')
    taskName = jsonData.get('name')
    taskNote = jsonData.get('note')

    try:
        createTask(
            user.id,
            fileId,
            toolId,
            materialId,
            taskName,
            taskNote
        )
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The task was successfully created'}, 200

@taskBlueprint.route('/<int:task_id>/status', methods=['PUT'])
@token_required
@only_admin
def updateExistingTaskStatus(admin, task_id):
    try:
        validate(instance=request.json, schema=UPDATE_TASK_STATUS_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    adminId = admin.id
    taskStatus = request.json.get('status')
    cancellationReason = request.json.get('cancellation_reason')

    try:
        updateTaskStatus(
            task_id,
            taskStatus,
            adminId,
            cancellationReason
        )
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The task status was successfully updated'}, 200

@taskBlueprint.route('/<int:task_id>', methods=['PUT'])
@token_required
def updateExistingTask(user, task_id):
    try:
        validate(instance=request.json, schema=UPDATE_TASK_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    jsonData = request.json
    fileId = jsonData.get('file_id')
    toolId = jsonData.get('tool_id')
    materialId = jsonData.get('material_id')
    taskName = jsonData.get('name')
    taskNote = jsonData.get('note')
    taskPriority = jsonData.get('priority')

    try:
        updateTask(
            task_id,
            user.id,
            fileId,
            toolId,
            materialId,
            taskName,
            taskNote,
            taskPriority
        )
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The task was successfully updated'}, 200

@taskBlueprint.route('/<int:task_id>', methods=['DELETE'])
def removeExistingTask(task_id):
    try:
        removeTask(task_id)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The task was successfully removed'}, 200
