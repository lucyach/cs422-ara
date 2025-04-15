"""
Server Manager Module

Used for flask

"""

from flask import Flask, request, jsonify
from database_manager import DatabaseManager

app = Flask("ARA")
db = DatabaseManager()

@app.route('/save_notes', methods=['POST'])
def save_test():
    content = request.json
    user_id = content.get("user_id")
    data = content.get("data")
