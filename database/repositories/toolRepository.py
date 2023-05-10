from database.base import db
from database.models.tool import Tool

def createTool(name, description):
    # Create the tool
    newTool = Tool(name, description)

    # Persist data in DB
    db.session.add(newTool)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The tool was successfully created!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return

def getAllTools():
    # Get data from DB
    tools = []
    try:
        tools = db.session.query(Tool).all()
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

    return tools

def updateTool(id, name, description):
    # Get tool from DB
    try:
        tool = db.session.query(Tool).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not tool:
        raise Exception(f'Tool with ID {id} was not found')

    # Update the tool's info
    tool.name = name
    tool.description = description

    # Commit changes in DB
    try:
        db.session.commit()
        print('The tool was successfully updated!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()

def removeTool(id):
    # Get tool from DB
    try:
        tool = db.session.query(Tool).get(id)
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    if not tool:
        raise Exception(f'Tool with ID {id} was not found')

    # Remove the tool
    db.session.delete(tool)

    # Commit changes in DB
    try:
        db.session.commit()
        print('The tool was successfully removed!')
    except Exception as error:
        raise Exception(str(error.orig) + " for parameters" + str(error.params))

    # Close db.session
    db.session.close()