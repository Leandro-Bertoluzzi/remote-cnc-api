from authMiddleware import GetUserDep
from core.cncworker.app import app
import core.cncworker.utils as worker
from core.grbl.types import ParserState, Status
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal

workerRoutes = APIRouter(prefix="/worker", tags=["Worker"])


class TaskStatusResponseModel(BaseModel):
    status: Literal['PENDING', 'STARTED', 'RETRY', 'FAILURE', 'SUCCESS', 'PROGRESS']
    percentage: Optional[int]
    progress: Optional[int]
    total_lines: Optional[int]
    cnc_status: Optional[Status]
    cnc_parserstate: Optional[ParserState]
    result: Optional[bool]
    error: Optional[str]


class WorkerStatusResponseModel(BaseModel):
    connected: bool
    running: bool
    available: bool
    stats: dict
    registered_tasks: Optional[worker.WorkerTaskList]
    active_tasks: Optional[worker.WorkerTaskList]


@workerRoutes.get('/status/{worker_task_id}')
def get_worker_task_status(
    user: GetUserDep,
    worker_task_id: str
) -> TaskStatusResponseModel:
    if not worker.is_worker_on():
        raise HTTPException(400, detail='Worker is off')

    try:
        task_state = app.AsyncResult(worker_task_id)
        task_info = task_state.info
        task_status = task_state.status
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    response = {
        'status': task_status
    }

    if task_state.failed():
        # If the task raised an exception, 'info' will be the exception instance
        response['error'] = str(task_info)
        return response

    if task_status == 'PROGRESS':
        response['percentage'] = task_info.get('percentage')
        response['progress'] = task_info.get('progress')
        response['total_lines'] = task_info.get('total_lines')
        response['cnc_status'] = task_info.get('status')
        response['cnc_parserstate'] = task_info.get('parserstate')
        return response

    if task_state.result:
        response['result'] = task_state.result
    return response


@workerRoutes.get('/check/on')
def check_worker_on(user: GetUserDep):
    """Returns whether the worker process is running.
    """
    return { 'is_on': worker.is_worker_on() }


@workerRoutes.get('/check/running')
def check_worker_running(user: GetUserDep):
    """Returns whether the worker process is working on a task.
    """
    return { 'running': worker.is_worker_running() }


@workerRoutes.get('/check/available')
def check_worker_available(user: GetUserDep):
    """Returns whether the worker process is available to start working on a task.
    """
    return { 'available': worker.is_worker_available() }


@workerRoutes.get('/status')
def get_worker_status(user: GetUserDep) -> WorkerStatusResponseModel:
    """Returns the worker status.
    """
    return worker.get_worker_status()
