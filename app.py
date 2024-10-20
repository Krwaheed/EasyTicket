
import os
from flask import flash
from datetime import datetime
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
    cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
    if cursor.fetchone():
        print("Error: Username already exists.")
        return

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

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
        cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['user_id'] = user['user_id']  # Set user_id in session
            return redirect(url_for('user_dashboard'))
        else:
            return redirect(url_for('home'))
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
        "x-rapidapi-key": "302ec63930msh5311bb73e188dc3p112effjsnb788b6f9f595",
        "x-rapidapi-host": "real-time-events-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_user_recommendations(username):
    """Fetch recommended events based on user interests."""
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.interest_name FROM user_interests ui
        JOIN interests i ON ui.interest_id = i.interest_id
        JOIN users u ON ui.user_id = u.user_id
        WHERE u.username = %s
    """, (username,))
    interests = cursor.fetchall()
    print("Interests fetched:", interests)

    recommended_events = []
    for interest in interests:
        print("Fetching events for interest:", interest['interest_name'])
        event = fetch_real_time_events(interest['interest_name'])
        print("Event fetched:", event)
        if event and event.get('data'):
            # Add only the first event of each interest to the recommendations
            recommended_events.append(event['data'][0])

    print("Recommended events:", recommended_events)
    return recommended_events



@app.route('/user-dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    query = request.form.get('query') if request.method == 'POST' else "Concerts in San-Francisco"
    # Fetch events based on the search query
    events_data = fetch_real_time_events(query)
    if events_data:
        events = events_data.get('data', [])
    else:
        events = []

    # Fetch user-specific recommendations
    recommendations = get_user_recommendations(username)

    # Fetch saved events from database
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT event_id, event_name, event_date, location 
        FROM saved_events 
        WHERE user_id = %s
    """, (session.get('user_id'),))
    saved_events = cursor.fetchall()
    cursor.close()

    return render_template('user-dashboard.html', username=session['username'], events=events, saved_events=saved_events,recommendations=recommendations, query=query)


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

        cursor = db.cursor()  # Use the established connection
        try:
            # Insert user into the users table
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            user_id = cursor.lastrowid  # Get the ID of the newly created user

            # Save selected interests
            selected_interests = request.form.getlist('interests')
            for interest in selected_interests:
                cursor.execute("INSERT INTO user_interests (user_id, interest_id) VALUES (%s, %s)",
                               (user_id, interest))

            db.commit()  # Commit changes to the database
            return jsonify({'status': 'success', 'redirect_url': url_for('home')})  # JSON response with redirect URL
        except mysql.connector.Error as err:
            db.rollback()  # Rollback in case of error
            return jsonify({'status': 'error', 'message': str(err)})
        finally:
            cursor.close()  # Close the cursor

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
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
            session['admin-username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('adminLogin'))
    return render_template('adminLogin.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin-username' in session:

        return render_template('admin-dashboard.html', admin_username=session['admin-username'])
    else:

        return redirect(url_for('adminLogin'))

@app.route('/api/admin/session', methods=['GET'])
def admin_session():
    if 'admin-username' in session:
        return jsonify({'username': session['admin-username']})
    else:
        return jsonify({'username': None}), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    # Checking if admin is logged in
    if 'admin-username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='easyticket'
    )

    # Checking if the connection is lost and reconnect
    if not connection.is_connected():
        connection.reconnect(attempts=3, delay=2)

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, email FROM users")
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if 'admin-username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='easyticket'
    )

    if not connection.is_connected():
        connection.reconnect(attempts=3, delay=2)

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()  # Commit the deletion
        if cursor.rowcount == 0:  # No rows were affected (user not found)
            return jsonify({'error': 'User not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'User deleted successfully'}), 200



@app.route('/api/events', methods=['GET'])
def get_events():
    if 'admin-username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM events")
    events = cursor.fetchall()
    return jsonify([{'id': event['id'], 'name': event['name']} for event in events])


#*********saved events**********
@app.route('/save-event', methods=['POST'])
def save_event():
    print("Received form data:", request.form)

    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Extract event details from form data
    event_id = request.form.get('event_id')
    event_name = request.form.get('event_name')
    start_time = request.form.get('start_time')
    venue_name = request.form.get('venue_name')
    full_address = request.form.get('full_address')

    # Check if required fields are provided
    if not event_id or not event_name or not start_time or not venue_name or not full_address:
        flash('Missing event data. Please provide all event details.')
        return redirect(url_for('user_dashboard'))

    print("Event Name:", event_name)


    try:

        formatted_event_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        flash('Invalid event date format.')
        return redirect(url_for('user_dashboard'))

    try:
        cursor = db.cursor()

        query = """
            INSERT INTO saved_events (user_id, event_id, event_name, event_date, location) 
            VALUES (%s, %s, %s, %s, %s)
        """
        # Combine venue name and full address for location
        location = f"{venue_name}, {full_address}"

        cursor.execute(query, (session['user_id'], event_id, event_name, formatted_event_date, location))
        db.commit()
        flash('Event saved successfully!')
    except mysql.connector.Error as err:
        print('Database Error:', err)
        flash('Error saving event. Please try again later.')
    finally:
        cursor.close()

    return redirect(url_for('user_dashboard'))


#*****remove events*******
@app.route('/remove-event', methods=['POST'])
def remove_event():
    if 'user_id' not in session:
        flash('Please login to continue.')
        return redirect(url_for('login'))

    event_id = request.form.get('event_id')
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM saved_events WHERE event_id = %s AND user_id = %s", (event_id, session['user_id']))
        db.commit()
        flash('Event removed successfully!')
    except mysql.connector.Error as err:
        db.rollback()
        flash(f'Error removing event: {err}')
    finally:
        cursor.close()

    return redirect(url_for('user_dashboard'))




if __name__ == '__main__':
    app.run(debug=True)