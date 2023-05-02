from database.base import db
from database.models.file import File

def createFile(userId, fileName, fileNameSaved):
    # Create the file entry
    filePath = f'{userId}/{fileNameSaved}'
    newFile = File(userId, fileName, filePath)

    # Persist data in DB
    db.session.add(newFile)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The file was successfully created!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return

def getAllFiles():
    # Get data from DB
    files = []
    try:
        files = db.session.query(File).all()
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return files

def getFileById(id):
    # Get file from DB
    try:
        file = db.session.query(File).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not file:
        raise Exception(f'File with ID {id} was not found')
    
    return file

def updateFile(id, userId, fileName, fileNameSaved):
    # Get file from DB
    file = getFileById(id)

    # Update the file's info
    file.user_id = userId
    file.file_path = f'{userId}/{fileNameSaved}'
    file.file_name = fileName

    # Commit changes in DB
    try:
        db.session.commit()
        print('The file was successfully updated!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

def removeFile(id):
    # Get file from DB
    file = getFileById(id)

    # Remove the file
    db.session.delete(file)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The file was successfully removed!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()