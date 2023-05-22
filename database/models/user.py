from database.base import db

VALID_ROLES = ['user', 'admin']

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    # Virtual columns
    tasks = db.relationship('Task', backref='user', foreign_keys='Task.user_id')
    files = db.relationship('File', backref='user')

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return f"<User: {self.name}, email: {self.email}, role: {self.role}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }
