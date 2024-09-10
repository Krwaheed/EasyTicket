from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy

# Define User model for 'users' table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing ID
    username = db.Column(db.String(50), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email
    password = db.Column(db.String(200), nullable=False)  # Hashed password

    # Constructor to initialize user
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
