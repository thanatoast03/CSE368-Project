from flask import Flask, jsonify, request, make_response, redirect, url_for
from pymongo import MongoClient
import bcrypt
import secrets
import hashlib

app = Flask(__name__)

mongo_client = MongoClient("mongo")
db = mongo_client["CSE368"]
user_collection = db['users']


@app.route('/')
def index():
    user_token = request.cookies.get('user_token')
    if user_token:
        user = user_collection.find_one({'authentication_token': hashlib.sha256(user_token.encode()).hexdigest()})
        if user:
            return jsonify({
                'username': user.get('username'),
                'theme': user.get('theme', 'light'),
                'xsrf_token': user['xsrf_token']
            }), 200
    return jsonify({'error': 'Not logged in'}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    password_confirm = data.get('confirmPassword')

    if password != password_confirm:
        return jsonify({'error': 'Passwords do not match'}), 400

    if user_collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    if not misc.is_valid_password(password):
        return jsonify({'error': 'Invalid password format'}), 400

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode(), salt)

    user_collection.insert_one({'username': username, 'password': hashed_pwd, 'email': email})
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = user_collection.find_one({'username': username})
    if user and bcrypt.checkpw(password.encode(), user['password']):
        user_token = secrets.token_hex(15)
        hashed_token = hashlib.sha256(user_token.encode()).hexdigest()
        xsrf_token = secrets.token_urlsafe(15)

        user_collection.update_one({"username": username},
                                   {"$set": {"authentication_token": hashed_token, "xsrf_token": xsrf_token}})

        response = jsonify({
            'username': user.get('username'),
            'xsrf_token': xsrf_token
        })
        response.set_cookie("user_token", user_token, httponly=True, max_age=3600)
        return response, 200
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    user_token = request.cookies.get('user_token')
    if user_token:
        user_collection.update_one({"authentication_token": hashlib.sha256(user_token.encode()).hexdigest()},
                                   {"$unset": {"authentication_token": "", "xsrf_token": ""}})
        response = jsonify({'message': 'Logged out'})
        response.set_cookie('user_token', '', expires=0, httponly=True)
        return response, 200
    return jsonify({'error': 'Not logged in'}), 401


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
