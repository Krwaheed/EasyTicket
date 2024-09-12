import os
import mysql.connector
from flask import render_template, Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',  # Ensure this is your correct MySQL username
    password='',  # Ensure this is your correct MySQL password
    database='easyticket'  # Ensure this is your correct database name
)


# Existing routes...

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
            return redirect(url_for('home'))  # Redirect to home after signup
        except mysql.connector.Error as err:
            return f"Error: {err}"
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))


@app.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('adminLogin.html')
    elif request.method == 'POST':
        admin_username = request.form['admin-username']
        admin_password = request.form['admin-password']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username = %s", (admin_username,))
        admin = cursor.fetchone()

        if admin and check_password_hash(admin['password'], admin_password):
            session['admin_logged_in'] = True  # Set admin session
            return redirect(url_for('admin_dashboard'))
        else:
            return "Login Failed"

    return redirect(url_for('admin_dashboard'))


@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin_logged_in' in session:
        return render_template('admin-dashboard.html')
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)
