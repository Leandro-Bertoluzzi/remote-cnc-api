from database.base import db
from datetime import datetime

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    file_path = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Virtual columns
    tasks = db.relationship('Task', backref='file')

    def __init__(self, user_id, file_name, file_path, created_at=datetime.now()):
        self.user_id = user_id
        self.file_name = file_name
        self.file_path = file_path
        self.created_at = created_at

    def __repr__(self):
        return f"<File: {self.file_name}, path: {self.file_path}, user ID: {self.user_id}, created at: {self.created_at}>"

    def serialize(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "user_id": self.user_id,
            "user": self.user.name,
            "file_path": self.file_path,
            "created_at": self.created_at
        }
