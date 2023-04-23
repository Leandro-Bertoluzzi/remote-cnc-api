import bcrypt
from database.base import db
from database.models.user import User, VALID_ROLES

def createUser(name, email, password, role):
    # Validates the input
    if role not in VALID_ROLES:
        print(f'ERROR: Role {role} is not valid')
        return

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
        print(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

def getAllUsers():
    # Get data from DB
    users = []
    try:
        users = db.session.query(User).all()
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return users

def updateUser(id, name, email, password, role):
    # Validates the input
    if role not in VALID_ROLES:
        print(f'ERROR: Role {role} is not valid')
        return

    # Get user from DB
    try:
        user = db.session.query(User).get(id)
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))
        return

    # Update the user's info
    user.name = name
    user.email = email
    user.role = role

    # Commit changes in DB
    try:
        db.session.commit()
        print('The user was successfully updated!')
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

def removeUser(id):
    # Get user from DB
    try:
        user = db.session.query(User).get(id)
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))
        return

    # Remove the user
    db.session.delete(user)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The user was successfully removed!')
    except Exception as error:
        print(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()