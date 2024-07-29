from flask import Flask
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management
app.permanent_session_lifetime = timedelta(days=5)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Import routes after creating the app
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
