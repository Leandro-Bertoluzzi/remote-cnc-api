from database.base import db
from database.models.task import Task

def createTask(userId, fileId, name, status, priority):
    # Create the task
    newTask = Task(userId, fileId, name, status, priority)

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
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return tasks

def updateTask(id, userId, fileId, name, status, priority):
    # Get task from DB
    try:
        task = db.session.query(Task).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not task:
        raise Exception(f'Task with ID {id} was not found')

    # Update the task's info
    task.file_id = fileId
    task.user_id = userId
    task.name = name
    task.status = status
    task.priority = priority

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
