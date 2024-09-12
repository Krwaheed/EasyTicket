
import os
import mysql.connector
from flask import render_template, Flask, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Establishes connection to the database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='easyticket'
)


def add_admin(username, password):
    """Function to add an admin securely without a web interface."""
    cursor = db.cursor(dictionary=True)
    # Check if the username already exists
    cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
    if cursor.fetchone():
        print("Error: Username already exists.")
        return
    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    # Insert new admin
    try:
        cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
        print("Admin added successfully.")
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        cursor.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['username'] = username  # Store username in session
            return redirect(url_for('user_dashboard'))
        else:
            return redirect(url_for('home'))  # Redirect to home on failure
    return render_template('login.html')


@app.route('/user-dashboard')
def user_dashboard():
    if 'username' in session:
        return render_template('user-dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle the form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            db.commit()
            return jsonify({'status': 'success', 'redirect_url': url_for('home')})  # JSON response with redirect URL
        except mysql.connector.Error as err:
            return jsonify({'status': 'error', 'message': str(err)})
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))


@app.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
        admin = cursor.fetchone()
        if admin and check_password_hash(admin['password'], password):
            session['admin-username'] = username  # Store admin username in session
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('admin_login'))  # Redirect to admin login on failure

    return render_template('adminLogin.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin-username' in session:
        # Render the dashboard page with the admin username passed to the template
        return render_template('admin-dashboard.html', admin_username=session['admin-username'])
    # Redirect to login page if not logged in
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)