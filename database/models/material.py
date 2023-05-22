from database.base import db
from datetime import datetime

class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    added_at = db.Column(db.DateTime)

    # Virtual columns
    tasks = db.relationship('Task', backref='material')

    def __init__(self, name, description, added_at=datetime.now()):
        self.name = name
        self.description = description
        self.added_at = added_at

    def __repr__(self):
        return f"<Material: {self.name}, description: {self.description}, added at: {self.added_at}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "added_at": self.added_at
        }
