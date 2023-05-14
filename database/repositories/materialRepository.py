from database.base import db
from database.models.material import Material

def createMaterial(name, description):
    # Create the material
    newMaterial = Material(name, description)

    # Persist data in DB
    db.session.add(newMaterial)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The material was successfully created!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return

def getAllMaterials():
    # Get data from DB
    materials = []
    try:
        materials = db.session.query(Material).all()
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return materials

def updateMaterial(id, name, description):
    # Get material from DB
    try:
        material = db.session.query(Material).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not material:
        raise Exception(f'Material with ID {id} was not found')

    # Update the material's info
    material.name = name
    material.description = description

    # Commit changes in DB
    try:
        db.session.commit()
        print('The material was successfully updated!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

def removeMaterial(id):
    # Get material from DB
    try:
        material = db.session.query(Material).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not material:
        raise Exception(f'Material with ID {id} was not found')

    # Remove the material
    db.session.delete(material)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The material was successfully removed!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()