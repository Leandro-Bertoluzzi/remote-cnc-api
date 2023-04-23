from flask import Blueprint, jsonify
from database.repositories.userRepository import getAllUsers
from utilities.utils import serializeList

userBlueprint = Blueprint('userBlueprint', __name__)

@userBlueprint.route('/', methods=['GET'])
@userBlueprint.route('/all', methods=['GET'])
def getUsers():
    users = serializeList(getAllUsers())
    return jsonify(users)