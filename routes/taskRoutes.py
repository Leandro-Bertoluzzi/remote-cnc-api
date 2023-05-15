from flask import Blueprint, jsonify, request
from database.repositories.taskRepository import getAllTasks, createTask, updateTask, removeTask
from utilities.utils import serializeList
from database.models.task import VALID_STATUSES
from jsonschema import validate

taskBlueprint = Blueprint('taskBlueprint', __name__)

TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'file_id': {'type': 'integer'},
        'name': {'type': 'string'},
        'status': {'type': 'string', 'enum': VALID_STATUSES},
        'priority': {'type': 'integer'},
    },
    'required': ['name', 'status', 'priority'],
}

@taskBlueprint.route('/', methods=['GET'])
@taskBlueprint.route('/all', methods=['GET'])
def getTasks():
    tasks = serializeList(getAllTasks())
    return jsonify(tasks)

@taskBlueprint.route('/', methods=['POST'])
def createNewTask():
    try:
        validate(instance=request.json, schema=TASK_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    userId = request.json['user_id']
    fileId = request.json['file_id']
    taskName = request.json['name']
    taskStatus = request.json['status']
    taskPriority = request.json['priority']

    try:
        createTask(userId, fileId, taskName, taskStatus, taskPriority)
    except Exception as error:
        return {'Error': str(error)}, 400

    return {'success': 'The task was successfully created'}, 200

@taskBlueprint.route('/<int:task_id>', methods=['PUT'])
def updateExistingTask(task_id):
    try:
        validate(instance=request.json, schema=TASK_SCHEMA)
    except Exception as error:
        return {'Error': error.message}, 400

    userId = request.json['user_id']
    fileId = request.json['file_id']
    taskName = request.json['name']
    taskStatus = request.json['status']
    taskPriority = request.json['priority']

    try:
        updateTask(task_id, userId, fileId, taskName, taskStatus, taskPriority)
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
