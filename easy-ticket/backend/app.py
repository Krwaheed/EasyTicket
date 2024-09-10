from flask import Flask
from models.user import db
from routes.auth import auth_routes
from utils.database import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/easyticket_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize the database
init_db(app)

# Register authentication routes
app.register_blueprint(auth_routes)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
