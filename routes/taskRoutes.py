from authMiddleware import GetAdminDep, GetUserDep
from core.database.models import StatusType
from core.database.repositories.taskRepository import TaskRepository
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from utilities.utils import serializeList

taskRoutes = APIRouter()


class TaskCreateModel(BaseModel):
    name: str
    file_id: int
    tool_id: int
    material_id: int
    note: str = ''


class TaskUpdateStatusModel(BaseModel):
    status: StatusType
    cancellation_reason: str = ''


class TaskUpdateModel(BaseModel):
    file_id: Optional[int] = None
    tool_id: Optional[int] = None
    material_id: Optional[int] = None
    name: Optional[str] = None
    priority: Optional[int] = None
    note: Optional[str] = None


@taskRoutes.get('/tasks/')
def get_tasks_by_user(user: GetUserDep, status: str = 'all'):
    repository = TaskRepository()
    tasks = serializeList(repository.get_all_tasks_from_user(user.id, status))
    return tasks


@taskRoutes.get('/tasks/all')
def get_all_tasks(admin: GetAdminDep, status: str = 'all'):
    repository = TaskRepository()
    tasks = serializeList(repository.get_all_tasks(status))
    return tasks


@taskRoutes.post('/tasks/')
def create_new_task(request: TaskCreateModel, user: GetUserDep):
    fileId = request.file_id
    toolId = request.tool_id
    materialId = request.material_id
    taskName = request.name
    taskNote = request.note

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
        raise HTTPException(400, detail=str(error))

    return {'success': 'The task was successfully created'}


@taskRoutes.put('/tasks/{task_id}/status')
def update_task_status(task_id: int, request: TaskUpdateStatusModel, admin: GetAdminDep):
    taskStatus = request.status
    cancellationReason = request.cancellation_reason

    try:
        repository = TaskRepository()
        repository.update_task_status(
            task_id,
            taskStatus,
            admin.id,
            cancellationReason
        )
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The task status was successfully updated'}


@taskRoutes.put('/tasks/{task_id}')
def update_task(task_id: int, request: TaskUpdateModel, user: GetUserDep):
    fileId = request.file_id
    toolId = request.tool_id
    materialId = request.material_id
    taskName = request.name
    taskNote = request.note
    taskPriority = request.priority

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
        raise HTTPException(400, detail=str(error))

    return {'success': 'The task was successfully updated'}


@taskRoutes.delete('/tasks/{task_id}')
def remove_task(task_id: int, user: GetUserDep):
    try:
        repository = TaskRepository()
        repository.remove_task(task_id)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

    return {'success': 'The task was successfully removed'}
