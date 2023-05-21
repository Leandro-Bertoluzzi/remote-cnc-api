from flask import Blueprint, jsonify, request
from services.serialService import SerialService
from services.gcodeService import validateGcodeBlock
import time

cncBlueprint = Blueprint('cncBlueprint', __name__)

@cncBlueprint.route('/command', methods=['POST'])
def sendCodeToExecute():
    # Get code from request body
    code = request.json['command']

    # Validate the code prior to send it
    try:
        validateGcodeBlock(code)
    except Exception as error:
        return {'Error': str(error)}, 400

    serial = SerialService()

    # Establish the serial connection
    # Replace 'COMx' with the appropriate port name
    # - On Windows, the port name typically starts with 'COM' (e.g., 'COM1', 'COM2').
    # - On macOS, it often starts with '/dev/cu.usbmodem' or '/dev/tty.usbmodem'.
    # - On Linux, it can be something like '/dev/ttyUSB0' or '/dev/ttyACM0'.
    # TODO: Set the port name as an environment variable
    try:
        serial.startConnection('COM6', baudrate=9600, timeout=5)
    except Exception as error:
        return {'Error': 'Could not start connection. Check if port is already used.'}, 400

    # Stream G-code to GRBL
    result = serial.streamBlock(code)

    # Close the serial connection
    serial.stopConnection()

    return { 'result': result }, 200
