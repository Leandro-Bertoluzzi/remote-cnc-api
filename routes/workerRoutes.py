from authMiddleware import GetUserDep
from celery.result import AsyncResult
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


@workerRoutes.get('/status/{worker_task_id}')
def get_worker_task_status(
    user: GetUserDep,
    worker_task_id: str
) -> TaskStatusResponseModel:
    try:
        task_state = AsyncResult(worker_task_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    task_info = task_state.info

    response = {
        'status': task_state.status
    }

    if task_state.failed():
        # If the task raised an exception, 'info' will be the exception instance
        response['error'] = str(task_info)
        return response

    if task_state.status == 'PROGRESS':
        response['percentage'] = task_info.get('percentage')
        response['progress'] = task_info.get('progress')
        response['total_lines'] = task_info.get('total_lines')
        response['cnc_status'] = task_info.get('status')
        response['cnc_parserstate'] = task_info.get('parserstate')

    if task_state.result:
        response['result'] = task_state.result
    return response
