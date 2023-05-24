from database.base import db
from database.models.file import File
from database.models.user import User

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
        raise Exception('Error creating the file in the DB')

    # Close db.session
    db.session.close()

    return

def getAllFilesFromUser(user_id):
    # Get data from DB
    try:
        user = db.session.query(User).get(user_id)
    except Exception as error:
        raise Exception('Error looking for user in the DB')

    for file in user.files:
            print(f'> {file.user}')
    print('----')

    # Close db.session
    db.session.close()

    return user.files

def getAllFiles():
    # Get data from DB
    try:
        files = db.session.query(File).all()
    except Exception as error:
        raise Exception('Error looking for files in the DB')

    for file in files:
            print(f'> {file.user}')
    print('----')

    # Close db.session
    db.session.close()

    return files

def getFileById(id):
    # Get file from DB
    try:
        file = db.session.query(File).get(id)
    except Exception as error:
        raise Exception(f'Error looking for file with ID {id} in the DB')

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
        raise Exception(f'Error updating file with ID {id} in the DB')

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
        raise Exception(f'Error removing file with ID {id} from the DB')

    # Close db.session
    db.session.close()
