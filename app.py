from flask import Flask
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

@app.route('/')
def index():
    return "Hello from the Python Flask App!"

@app.route('/db')
def db_status():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return f"Connected to PostgreSQL, version: {db_version}"
    else:
        return "Failed to connect to the database."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)