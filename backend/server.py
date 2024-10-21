from flask import Flask, request, make_response, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt
import secrets
import hashlib
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = OPENAI_API_KEY


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

mongo_client = MongoClient("mongo")
db = mongo_client["CSE368"]
user_collection = db['users']
chat_collection = db['chats']

@app.route('/')
def index():
    return jsonify(message="Welcome to the homepage"), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    password_confirm = data.get('confirm_password')

    if password != password_confirm:
        return jsonify({"error": "Passwords do not match"}), 400

    if user_collection.find_one({'username': username}):
        return jsonify({"error": "Username already exists"}), 400

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode(), salt)

    user_collection.insert_one({'username': username, 'password': hashed_pwd, 'email': email})
    return jsonify(message="User registered successfully"), 201

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

        user_collection.update_one({"username": username}, {"$set": {"authentication_token": hashed_token, "xsrf_token": xsrf_token}})

        response = make_response(jsonify(message="Login successful"))
        response.set_cookie(
            "user_token",
            user_token,
            httponly=True,
            max_age=3600,
            secure=False,
            path='/'
        )
        return response
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    user_token = request.cookies.get('user_token')
    if user_token:
        user_collection.update_one({"authentication_token": hashlib.sha256(user_token.encode()).hexdigest()}, {"$unset": {"authentication_token": "", "xsrf_token": ""}})
        response = make_response(jsonify(message="Logged out successfully"))
        response.set_cookie('user_token', '', expires=0, httponly=True)
        return response
    return jsonify({"error": "No user token found"}), 400


@app.route('/chat', methods=['POST'])
def handle_chat():
    user_token = request.cookies.get('user_token')
    if not user_token:
        return jsonify({"error": "No user token found"}), 401

    user = user_collection.find_one({"authentication_token": hashlib.sha256(user_token.encode()).hexdigest()})
    if not user:
        return jsonify({"error": "Invalid user token"}), 401

    username = user['username']
    user_input = request.json.get('message')

    # Use the new OpenAI client to create a chat completion
    response = OpenAI().chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )

    # Access the AI's response and usage data
    ai_response = response.choices[0].text
    usage_data = dict(response).get('usage')

    # Log the usage data if needed
    print("Usage Data:", usage_data)

    # Save the chat to the database
    chat_collection.insert_one({
        "username": username,
        "user_message": user_input,
        "ai_response": ai_response
    })

    return jsonify({"response": ai_response})


@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    user_token = request.cookies.get('user_token')
    if not user_token:
        return jsonify({"error": "No user token found"}), 401

    user = user_collection.find_one({"authentication_token": hashlib.sha256(user_token.encode()).hexdigest()})
    if not user:
        return jsonify({"error": "Invalid user token"}), 401

    username = user['username']
    chat_history = chat_collection.find({"username": username})

    chat_history_list = [{"user_message": chat["user_message"], "ai_response": chat["ai_response"]} for chat in chat_history]

    return jsonify(chatHistory=chat_history_list), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
