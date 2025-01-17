from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup function
def init_db():
    conn = sqlite3.connect('plans.db')  # Connect to SQLite database (it will create the file if it doesn't exist)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# Function to get all plans
@app.route('/plans', methods=['GET'])
def get_plans():
    conn = sqlite3.connect('plans.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plans ORDER BY date_added DESC')
    plans = cursor.fetchall()
    conn.close()

    return jsonify([{'id': plan[0], 'text': plan[1], 'date_added': plan[2]} for plan in plans])

# Function to add a new plan
@app.route('/plans', methods=['POST'])
def add_plan():
    data = request.get_json()
    plan_text = data.get('text')
    if plan_text:
        conn = sqlite3.connect('plans.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO plans (text) VALUES (?)', (plan_text,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Plan added successfully'}), 201
    else:
        return jsonify({'error': 'Plan text is required'}), 400

# Function to delete a plan
@app.route('/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    conn = sqlite3.connect('plans.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM plans WHERE id = ?', (plan_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Plan deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Ensure Flask is available on 0.0.0.0 and port 5000
