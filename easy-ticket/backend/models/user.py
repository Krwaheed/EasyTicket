from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(50), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password = db.Column(db.String(200), nullable=False)  # Hashed password
    is_admin = db.Column(db.Boolean, default=False)  # Determines if the user is an admin

    # Initialize a new user
    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)  # Hash password for security
        self.is_admin = is_admin  # Defaults to False (not an admin)

    # Method to check if the password is correct
    def check_password(self, password):
        return check_password_hash(self.password, password)
