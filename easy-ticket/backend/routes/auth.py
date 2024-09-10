from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, db

auth_routes = Blueprint('auth', __name__)

# User signup route
@auth_routes.route('/signup', methods=['POST'])
def signup():
    # Extract user data from the POST request
    data = request.get_json()
    
    # Hash the user's password before storing
    hashed_password = generate_password_hash(data['password'], method='sha256')

    # Create a new user instance
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Respond with a success message
    return jsonify({"message": "User created successfully"}), 201

# User login route
@auth_routes.route('/login', methods=['POST'])
def login():
    # Extract login data from the POST request
    data = request.get_json()
    
    # Find the user in the database by email
    user = User.query.filter_by(email=data['email']).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password, data['password']):
        session['user_logged_in'] = True  # Set session to mark user as logged in
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401  # Respond with error if credentials are wrong

# Admin login route
@auth_routes.route('/api/admin-login', methods=['POST'])
def admin_login():
    # Extract admin login data
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and is an admin
    user = User.query.filter_by(username=username, is_admin=True).first()

    # If user is admin and password is correct, log in as admin
    if user and check_password_hash(user.password, password):
        session['admin_logged_in'] = True  # Set session for admin
        return jsonify({"message": "Admin login successful"}), 200
    
    # Respond with error if credentials are wrong or user is not admin
    return jsonify({"message": "Invalid credentials or not an admin"}), 401
