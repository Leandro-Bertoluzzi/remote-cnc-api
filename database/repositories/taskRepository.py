from database.base import db
from database.models.task import Task
from datetime import datetime

def createTask(
    userId,
    fileId,
    toolId,
    materialId,
    name,
    note
):
    task_args = [
        userId,
        fileId,
        toolId,
        materialId,
        name
    ]

    # Optional arguments
    if note:
        task_args.append(note)

    # Create the task
    newTask = Task(*task_args)

    # Persist data in DB
    db.session.add(newTask)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The task was successfully created!')
    except Exception as error:
        raise Exception('Error creating new task in DB')

    # Close db.session
    db.session.close()

    return

def getAllTasks():
    # Get data from DB
    tasks = []
    try:
        tasks = db.session.query(Task).all()
    except Exception as error:
        raise Exception('Error looking for tasks in DB')

    # Close db.session
    db.session.close()

    return tasks

def getTasksByStatus(status):
    # Get data from DB
    tasks = []
    try:
        tasks = db.session.query(Task).filter_by(status=status)
    except Exception as error:
        raise Exception(f'Error looking for tasks with status {status} in DB')

    # Close db.session
    db.session.close()

    return tasks

def updateTask(
    id,
    userId,
    fileId,
    toolId,
    materialId,
    name,
    note,
    priority
):
    # Get task from DB
    try:
        task = db.session.query(Task).get(id)
    except Exception as error:
        raise Exception(f'Error looking for task with ID {id} in DB')

    if not task or task.user_id != userId:
        raise Exception(f'Task with ID {id} was not found for this user')

    # Update the task's info
    task.file_id = fileId if fileId else task.file_id
    task.tool_id = toolId if toolId else task.tool_id
    task.material_id = materialId if materialId else task.material_id
    task.name = name if name else task.name
    task.note = note if note else task.note
    task.priority = priority if priority else task.priority

    # Commit changes in DB
    try:
        db.session.commit()
        print('The task was successfully updated!')
    except Exception as error:
        raise Exception(f'Error updating task with ID {id} in DB')

    # Close db.session
    db.session.close()

def updateTaskStatus(id, status, admin_id=None):
    # Get task from DB
    try:
        task = db.session.query(Task).get(id)
    except Exception as error:
        raise Exception(f'Error looking for task with ID {id} in DB')

    if not task:
        raise Exception(f'Task with ID {id} was not found for this user')

    approved = task.status == 'pending_approval' and status == 'on_hold'
    rejected = task.status == 'pending_approval' and status == 'rejected'

    task.status = status
    task.status_updated_at = datetime.now()

    if approved or rejected:
        task.admin_id = admin_id

    if status == 'pending_approval':
        task.admin_id = None

    # Commit changes in DB
    try:
        db.session.commit()
        print('The task status was successfully updated!')
    except Exception as error:
        raise Exception(f'Error updating status of task with ID {id} in DB')

    # Close db.session
    db.session.close()

def removeTask(id):
    # Get task from DB
    try:
        task = db.session.query(Task).get(id)
    except Exception as error:
        raise Exception(f'Error looking for task with ID {id} in DB')

    if not task:
        raise Exception(f'Task with ID {id} was not found')

    # Remove the task
    db.session.delete(task)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The task was successfully removed!')
    except Exception as error:
        raise Exception(f'Error removing task with ID {id} from DB')

    # Close db.session
    db.session.close()
