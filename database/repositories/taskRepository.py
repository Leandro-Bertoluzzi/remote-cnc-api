from database.base import db
from database.models.task import Task

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
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return

def getAllTasks():
    # Get data from DB
    tasks = []
    try:
        tasks = db.session.query(Task).all()
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters " + str(error.params))

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
    status,
    priority
):
    # Get task from DB
    try:
        task = db.session.query(Task).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters " + str(error.params))

    if not task:
        raise Exception(f'Task with ID {id} was not found')

    # Update the task's info
    task.file_id = fileId if fileId else task.file_id
    task.user_id = userId if userId else task.user_id
    task.tool_id = toolId if toolId else task.tool_id
    task.material_id = materialId if materialId else task.material_id
    task.name = name if name else task.name
    task.note = note if note else task.note
    task.status = status if status else task.status
    task.priority = priority if priority else task.priority

    # Commit changes in DB
    try:
        db.session.commit()
        print('The task was successfully updated!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

def removeTask(id):
    # Get task from DB
    try:
        task = db.session.query(Task).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not task:
        raise Exception(f'Task with ID {id} was not found')

    # Remove the task
    db.session.delete(task)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The task was successfully removed!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()
