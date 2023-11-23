from flask import Blueprint, jsonify, request
from jsonschema import validate

from authMiddleware import token_required, only_admin
from core.database.models import VALID_STATUSES
from core.database.repositories.taskRepository import TaskRepository
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
def getTasksByUser(user):
    try:
        validate(instance=request.args, schema=GET_TASK_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    status = request.args.get('status', 'all')

    repository = TaskRepository()
    tasks = serializeList(repository.get_all_tasks_from_user(user.id, status))
    return jsonify(tasks)

@taskBlueprint.route('/all', methods=['GET'])
@token_required
@only_admin
def getTasks(admin):
    try:
        validate(instance=request.args, schema=GET_TASK_SCHEMA)
    except Exception as error:
        return {'error': error.message}, 400

    status = request.args.get('status')

    repository = TaskRepository()
    tasks = serializeList(repository.get_all_tasks(status))
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
        repository = TaskRepository()
        repository.create_task(
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
        repository = TaskRepository()
        repository.update_task_status(
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
        repository = TaskRepository()
        repository.update_task(
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
        repository = TaskRepository()
        repository.remove_task(task_id)
    except Exception as error:
        return {'error': str(error)}, 400

    return {'success': 'The task was successfully removed'}, 200
