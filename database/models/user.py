import bcrypt
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
        self.role = role
        # Hashing the password
        self.password = self.encryptPassword(password)

    def encryptPassword(self, password: str):
        """Generates a hash for the password"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def validatePassword(self, testPassword: str):
        """Compares a given password with the actual one"""
        return bcrypt.checkpw(testPassword.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f"<User: {self.name}, email: {self.email}, role: {self.role}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }
