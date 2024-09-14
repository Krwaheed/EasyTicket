
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
    return render_template('index.html')


#*************API*************
def fetch_real_time_events(query="Concerts in San-Francisco"):
    import requests
    url = "https://real-time-events-search.p.rapidapi.com/search-events"

    querystring = {
        "query": query,
        "date": "any",
        "is_virtual": "false",
        "start": "0"
    }

    headers = {
        "x-rapidapi-key": "466b2032ecmsh1ce2fa73d82434fp180e14jsnc743ba29a543",
        "x-rapidapi-host": "real-time-events-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        return None



@app.route('/user-dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Handle the event search query either from the form or use default
    query = request.form.get('query') if request.method == 'POST' else "Concerts in San-Francisco"

    # Fetch events based on the search query
    events_data = fetch_real_time_events(query)

    if events_data:
        events = events_data.get('data', [])
    else:
        events = []  # Default to an empty list if fetch fails

    # Render the dashboard template with events data
    return render_template('user-dashboard.html', username=session['username'], events=events, query=query)


#************ sing up for user*************
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

#********************** Admin stuff ***********************


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
            return redirect(url_for('adminLogin'))
    return render_template('adminLogin.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin-username' in session:
        # Render the dashboard page with the admin username passed to the template
        return render_template('admin-dashboard.html', admin_username=session['admin-username'])
    else:
        # Redirect to login page if not logged in
        return redirect(url_for('adminLogin'))

@app.route('/api/admin/session', methods=['GET'])
def admin_session():
    if 'admin-username' in session:
        return jsonify({'username': session['admin-username']})
    else:
        return jsonify({'username': None}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    if 'admin-username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/api/events', methods=['GET'])
def get_events():
    if 'admin-username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM events")  # Make sure you have an 'events' table with at least these fields
    events = cursor.fetchall()
    return jsonify([{'id': event['id'], 'name': event['name']} for event in events])






if __name__ == '__main__':
    app.run(debug=True)