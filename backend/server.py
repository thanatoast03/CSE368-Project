from flask import Flask, request, make_response, jsonify, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt, secrets, hashlib, os, sys # TODO: MIGHT WANNA REMOVE SYS
import google.generativeai as genai

INIT_PROMPT = """
You are a bot that helps students find out what classes students should take next. 
After this message, I will send information about 5 different majors from the university in 5 messages; 
MAKE SURE TO COUNT ALL 5 BEFORE STARTING. Understand that though students may be in a certain year, this 
does not guarantee that they will pass certain classes. After these 5 messages, the student will begin 
speaking with you. They will answer what their year and major is. Afterwards,
I want you to ask them what classes they are currently taking, then use the previous 
data I sent you to list out classes only from the next semester based on ones they have taken.
"""

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

mongo_client = MongoClient("mongo")
db = mongo_client["CSE368"]
user_collection = db['users']

model = None
chat = None

@app.route('/')
def index():
    # Return a message or redirect to login; adjust as needed
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

        user_collection.update_one({"username": username}, {"$set": {"authentication_token": hashed_token}})
        response = make_response(jsonify(message="Login successful"))
        response.set_cookie("user_token", user_token, httponly=True, max_age=3600)
        return response
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    user_token = request.cookies.get('user_token')
    if user_token:
        user_collection.update_one({"authentication_token": hashlib.sha256(user_token.encode()).hexdigest()}, {"$unset": {"authentication_token": ""}})
        response = make_response(jsonify(message="Logged out successfully"))
        response.set_cookie('user_token', '', expires=0, httponly=True, samesite=None, secure=False)
        return response
    return jsonify({"error": "No user token found"}), 400

@app.route('/chatInitialize')
def chatInitialize():
    print("THEY CALLED CHAT INITIALIZE!!!!!!!!1", file=sys.stderr)
    try:
        load_dotenv()

        # Access environment variable
        api_key = os.getenv("API_KEY")
        genai.configure(api_key=api_key)

        global model
        global chat
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                # {"role": "user", "parts": "<ignore for now, will be user messages later>"},
                # {"role": "model", "parts": "Great to meet you. What would you like to know?"},
                # TODO: fill this in with the chat history later on
            ]
        )
        response = chat.send_message(INIT_PROMPT)
        print(response.text, file=sys.stderr)

        with open('./classes/Computer-Engineering-BS.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Computer Engineering BS program: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/Computer-Science-BA.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Computer Science BA program: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/Computer-Science-BS_Computer-Science-and-Engineering-MS.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Computer Science and Engineering BS program: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/Computer-Science-BS_MBA.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Computer Science BS MBA program: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/Computer-Science-BS.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Computer Science BS program: {file_contents}")
            print(response.text, file=sys.stderr)

        if response.text:
            return jsonify({"text": response.text}), 200
        else:
            jsonify({"text": "No reply received from Gemini AI."}), 400
    
    except:
        raise

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    username = data.get('sender')
    text = data.get('text')

    try:
        response = chat.send_message(text)
        if response.text:
            return jsonify({"text": response.text}), 200
        else:
            jsonify({"text": "No reply received from Gemini AI."}), 400
    except:
        raise

    # TODO: store user history

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True) #debug=True)
