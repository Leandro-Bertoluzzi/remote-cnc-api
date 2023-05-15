from database.base import db
from datetime import datetime

VALID_STATUSES = [
    'pending_approval',
    'on_hold',
    'in_progress',
    'finished',
    'rejected'
]

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    file_id = db.Column(db.Integer)
    name = db.Column(db.String)
    status = db.Column(db.String)
    priority = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    approved_at = db.Column(db.DateTime)
    rejected_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)

    def __init__(self, user_id, file_id, name, status, priority, created_at=datetime.now()):
        self.user_id = user_id
        self.file_id = file_id
        self.name = name
        self.status = status
        self.priority = priority
        self.created_at = created_at

    def __repr__(self):
        return f"<Task: {self.name}, status: {self.status}, created at: {self.created_at}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "file_id": self.file_id,
            "name": self.name,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
            "approved_at": self.approved_at,
            "rejected_at": self.rejected_at,
            "finished_at": self.finished_at
        }
