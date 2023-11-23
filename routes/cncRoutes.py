from flask import Blueprint, jsonify, request
import time

from authMiddleware import token_required, only_admin
from config import SERIAL_PORT, SERIAL_BAUDRATE
from core.utils.serial import SerialService
from services.gcodeService import validateGcodeBlock

cncBlueprint = Blueprint('cncBlueprint', __name__)

@cncBlueprint.route('/command', methods=['POST'])
@token_required
@only_admin
def sendCodeToExecute(admin):
    # Get code from request body
    code = request.json['command']

    # Validate the code prior to send it
    try:
        validateGcodeBlock(code)
    except Exception as error:
        return {'Error': str(error)}, 400

    serial = SerialService()

    # Establish the serial connection
    try:
        serial.startConnection(
            port=SERIAL_PORT,
            baudrate=SERIAL_BAUDRATE,
            timeout=5
        )
    except Exception as error:
        return {'Error': 'Could not start connection. Check if port is already used.'}, 400

    # Stream G-code to GRBL
    result = serial.streamBlock(code)

    # Close the serial connection
    serial.stopConnection()

    return { 'result': result }, 200
