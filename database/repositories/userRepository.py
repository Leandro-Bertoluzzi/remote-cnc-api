from database.base import db
from database.models.user import User

def createUser(name, email, password, role):
    # Get user from DB
    try:
        user = db.session.query(User).filter_by(email=email).first()
    except Exception as error:
        raise Exception(f'Error looking for user with email {email} in the DB')

    if user:
        raise Exception(f'There is already a user registered with the email {email}')

    # Create the user
    newUser = User(name, email, password, role)

    # Persist data in DB
    db.session.add(newUser)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The user was successfully created!')
    except Exception as error:
        raise Exception('Error creating the user in the DB')

    # Close db.session
    db.session.close()

    return

def getAllUsers():
    # Get data from DB
    users = []
    try:
        users = db.session.query(User).all()
    except Exception as error:
        raise Exception('Error retrieving users from the DB')

    # Close db.session
    db.session.close()

    return users

def updateUser(id, name, email, password, role):
    # Get user from DB
    try:
        user = db.session.query(User).get(id)
    except Exception as error:
        raise Exception('Error looking for user in the DB')

    if not user:
        raise Exception(f'User with ID {id} was not found')

    # Update the user's info
    user.name = name
    user.email = email
    user.role = role

    # Commit changes in DB
    try:
        db.session.commit()
        print('The user was successfully updated!')
    except Exception as error:
        raise Exception('Error updating the user in the DB')

    # Close db.session
    db.session.close()

    return

def removeUser(id):
    # Get user from DB
    try:
        user = db.session.query(User).get(id)
    except Exception as error:
        raise Exception('Error looking for user in the DB')

    if not user:
        raise Exception(f'User with ID {id} was not found')

    # Remove the user
    db.session.delete(user)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The user was successfully removed!')
    except Exception as error:
        raise Exception('Error removing the user from the DB')

    # Close db.session
    db.session.close()

    return

def loginUser(email, password):
    # Get user from DB
    try:
        user = db.session.query(User).filter_by(email=email).first()
    except Exception as error:
        raise Exception(f'Error looking for user with email {email} in the DB')

    if not user:
        return None, f'User with email {email} was not found'

    if not user.validatePassword(password):
        return None, 'Wrong password'

    # Close db.session
    db.session.close()

    return user, ''
