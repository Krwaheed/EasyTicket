from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, db

# Create Blueprint for authentication routes
auth_routes = Blueprint('auth', __name__)

# Route for user signup
@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Get JSON data from request
    hashed_password = generate_password_hash(data['password'], method='sha256')  # Hash password

    # Create new user instance
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    
    # Save user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# Route for user login
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from request
    user = User.query.filter_by(email=data['email']).first()  # Find user by email

    # Check if user exists and password matches
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
