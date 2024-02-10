

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data and 'email' in data and 'password' in data:
        hashed_password = generate_password_hash(data['password'])
        mongo.db.users.insert_one({'email': data['email'], 'password': hashed_password})
        return jsonify({'message': 'User registered successfully', 'email': data['email']}), 201
    else:
        return jsonify({'message': 'Invalid data'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and 'email' in data and 'password' in data:
        user = mongo.db.users.find_one({'email': data['email']})
        if user and check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    else:
        return jsonify({'message': 'Invalid data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
