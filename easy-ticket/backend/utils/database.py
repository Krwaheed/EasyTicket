from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy

# Function to initialize the database
def init_db(app):
    # Configure the database URI (replace 'username', 'password', and 'easyticket_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/easyticket_db'
    
    # Disable modification tracking to save resources
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind the app to SQLAlchemy
    db.init_app(app)

    # Create all tables in the database (if not already created)
    with app.app_context():
        db.create_all()
