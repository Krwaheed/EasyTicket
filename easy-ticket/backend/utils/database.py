from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # Configure the database URI and disable tracking modifications
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourusername:yourpassword@localhost/easyticket_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Bind the SQLAlchemy instance to the app
    db.init_app(app)

    # Create tables if they don't already exist
    with app.app_context():
        db.create_all()
