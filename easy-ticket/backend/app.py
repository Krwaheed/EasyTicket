from flask import Flask, send_from_directory, render_template
from routes.auth import auth_routes
from utils.database import init_db
import os

app = Flask(__name__, 
            static_folder='../frontend',    # Serve static files from frontend directory
            template_folder='../frontend')  # Serve templates from frontend directory

# Initialize the database
init_db(app)

# Register authentication routes
app.register_blueprint(auth_routes)

# Serve the index page
@app.route('/')
def home():
    return render_template('index.html')  # Renders the index.html from frontend

@app.route('/signup')
def signup():
    return render_template('signup.html')  # Renders signup.html from frontend

@app.route('/admin')
def admin_login():
    return render_template('adminLogin.html')  # Renders adminLogin.html from frontend

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin-dashboard.html')  # Renders admin-dashboard.html from frontend

# Serve static files (CSS, JS, images) from the frontend directory
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
