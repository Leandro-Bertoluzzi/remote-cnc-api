import bcrypt
from database.base import db
from database.models.user import User

def createUser(name, email, password, role):
    # --- Encrypt password ---
    # Adding the salt to password
    salt = bcrypt.gensalt()
    # Hashing the password
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Create the user
    newUser = User(name, email, hashedPassword, role)

    # Persist data in DB
    db.session.add(newUser)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The user was successfully created!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return

def getAllUsers():
    # Get data from DB
    users = []
    try:
        users = db.session.query(User).all()
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return users

def updateUser(id, name, email, password, role):
    # Get user from DB
    try:
        user = db.session.query(User).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

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
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

def removeUser(id):
    # Get user from DB
    try:
        user = db.session.query(User).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not user:
        raise Exception(f'User with ID {id} was not found')

    # Remove the user
    db.session.delete(user)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The user was successfully removed!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()