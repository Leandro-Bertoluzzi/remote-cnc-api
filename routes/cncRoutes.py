from config import SERIAL_PORT, SERIAL_BAUDRATE
from core.cncworker.workerStatusManager import WorkerStoreAdapter
import core.cncworker.utils as worker
from core.utils.serial import SerialService
from core.worker import cncServer, COMMANDS_CHANNEL
from fastapi import APIRouter, HTTPException
from middleware.authMiddleware import GetAdminDep
from middleware.pubSubMiddleware import GetPubSub
from pydantic import BaseModel

cncRoutes = APIRouter(prefix="/cnc", tags=["CNC"])


class CncCommandModel(BaseModel):
    command: str


@cncRoutes.get('/ports')
def get_available_ports(admin: GetAdminDep):
    try:
        available_ports = SerialService.get_ports()
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'ports': available_ports}


@cncRoutes.post('/server')
def start_cnc_server(admin: GetAdminDep):
    if not worker.is_worker_on():
        raise HTTPException(400, detail='Worker desconectado')

    if not WorkerStoreAdapter.is_device_enabled():
        raise HTTPException(400, detail='Equipo deshabilitado')

    if worker.is_worker_running():
        raise HTTPException(400, detail='Equipo ocupado: Hay una tarea en progreso')

    worker_task = cncServer.delay(
        SERIAL_PORT,
        SERIAL_BAUDRATE
    )

    return {
        'success': 'Se abrió la conexión con el CNC',
        'worker_task_id': worker_task.task_id
    }


@cncRoutes.delete('/server')
async def stop_cnc_server(admin: GetAdminDep, redis: GetPubSub):
    if not worker.is_worker_on():
        raise HTTPException(400, detail='Worker desconectado')

    # TODO: Improve this...
    await redis.publish(COMMANDS_CHANNEL, 'M2')

    return {'success': 'Se finalizó la conexión con el CNC'}


@cncRoutes.post('/command')
async def send_code_to_execute(
    request: CncCommandModel,
    admin: GetAdminDep,
    redis: GetPubSub
):
    if not worker.is_worker_on():
        raise HTTPException(400, detail='Worker desconectado')

    if not worker.is_worker_running():
        raise HTTPException(400, detail='Debe iniciar la conexión con el servidor CNC')

    # Get code from request body
    code = request.command

    # Request command execution
    await redis.publish(COMMANDS_CHANNEL, code)

    return {'success': 'El comando fue enviado para su ejecución'}
