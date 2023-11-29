from authMiddleware import GetAdminDep
from config import SERIAL_PORT, SERIAL_BAUDRATE
from core.utils.serial import SerialService
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gcode import validateGcodeBlock

cncRoutes = APIRouter(prefix="/cnc", tags=["CNC"])


class CncCommandModel(BaseModel):
    command: str


@cncRoutes.post('/command')
def send_code_to_execute(request: CncCommandModel, admin: GetAdminDep):
    # Get code from request body
    code = request.command

    # Validate the code prior to send it
    try:
        validateGcodeBlock(code)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    serial = SerialService()

    # Establish the serial connection
    try:
        serial.startConnection(
            port=SERIAL_PORT,
            baudrate=SERIAL_BAUDRATE,
            timeout=5
        )
    except Exception:
        raise HTTPException(
            400,
            detail='Could not start connection. Check if port is already used.'
        )

    # Stream G-code to GRBL
    result = serial.streamBlock(code)

    # Close the serial connection
    serial.stopConnection()

    return {'result': result}
