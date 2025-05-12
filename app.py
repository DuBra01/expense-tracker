from flask import Flask, jsonify, request, render_template
from datetime import datetime
import csv
from pathlib import Path

app = Flask(__name__)

# Global Variables
expenses = []
budget = 0.0

# CSV file location (your specified path)
DATA_FILE = Path('/Users/janlelie/Desktop/Caltech AI & Machine Learning Bootcamp/Projects Repository/expenses.csv')

# Ensure CSV file exists with headers
def load_expenses():
    expenses.clear()
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
            writer.writeheader()
    else:
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append({
                    'date': row['date'],
                    'category': row['category'],
                    'amount': float(row['amount']),
                    'description': row['description']
                })

# Save expenses to CSV file
def save_expenses():
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
        writer.writeheader()
        writer.writerows(expenses)

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# API: Add expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')  # Validate date format
        amount = float(data['amount'])
        expense = {
            'date': data['date'],
            'category': data['category'],
            'amount': amount,
            'description': data['description']
        }
        expenses.append(expense)
        save_expenses()
        return jsonify({'status': 'success', 'message': 'Expense added successfully!'}), 200
    except (ValueError, KeyError):
        return jsonify({'status': 'error', 'message': 'Invalid input provided!'}), 400

# API: Retrieve expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

# API: Set monthly budget
@app.route('/set_budget', methods=['POST'])
def set_budget():
    global budget
    data = request.json
    try:
        budget = float(data['budget'])
        return jsonify({'status': 'success', 'budget': budget}), 200
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid budget amount!'}), 400

# API: Track budget status
@app.route('/track_budget', methods=['GET'])
def track_budget():
    total_expenses = sum(exp['amount'] for exp in expenses)
    remaining = budget - total_expenses
    status = "within_budget" if remaining >= 0 else "over_budget"
    return jsonify({
        'budget': budget,
        'total_expenses': total_expenses,
        'remaining': remaining,
        'status': status
    })

# Initialize data and run Flask server
if __name__ == '__main__':
    load_expenses()
    app.run(debug=True)