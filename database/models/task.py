from database.base import db
from datetime import datetime

# Enum values
VALID_STATUSES = [
    'pending_approval',
    'on_hold',
    'in_progress',
    'finished',
    'rejected'
]

# Constants
TASK_EMPTY_NOTE=''
TASK_DEFAULT_PRIORITY=0
TASK_INITIAL_STATUS='pending_approval'

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    status = db.Column(db.String)
    priority = db.Column(db.Integer)
    note = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    status_updated_at = db.Column(db.DateTime)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Virtual columns
    admin = db.relationship('User', foreign_keys=[admin_id])

    def __init__(
        self,
        user_id,
        file_id,
        tool_id,
        material_id,
        name,
        note=TASK_EMPTY_NOTE,
        status=TASK_INITIAL_STATUS,
        priority=TASK_DEFAULT_PRIORITY,
        created_at=datetime.now()
    ):
        self.user_id = user_id
        self.file_id = file_id
        self.tool_id = tool_id
        self.material_id = material_id
        self.name = name
        self.note = note
        self.status = status
        self.priority = priority
        self.created_at = created_at

    def __repr__(self):
        return f"<Task: {self.name}, status: {self.status}, created at: {self.created_at}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "priority": self.priority,
            "user_id": self.user_id,
            "user": self.user.name,
            "file_id": self.file_id,
            "file": self.file.file_name,
            "tool_id": self.tool_id,
            "tool": self.tool.name,
            "material_id": self.material_id,
            "material": self.material.name,
            "note": self.note,
            "created_at": self.created_at,
            "status_updated_at": self.status_updated_at,
            "admin_id": self.admin_id,
            "admin": self.admin.name
        }
