from flask import Flask, request, make_response, jsonify, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt, secrets, hashlib, os, sys # TODO: MIGHT WANNA REMOVE SYS
import google.generativeai as genai

INIT_PROMPT = """
You are a bot that helps students find out what classes students should take next. 
After this message, I will send information about 12 different majors from the university in 12 messages; 
MAKE SURE TO COUNT ALL 12 BEFORE STARTING. Understand that though students may be in a certain year, this 
does not guarantee that they will pass certain classes. After these 12 messages, the student will begin 
speaking with you. They will answer what their year and major is. Afterwards,
I want you to ask them what classes they are currently taking, then use the previous 
data I sent you to list out classes only from the next semester based on ones they have taken.
"""

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

mongo_client = MongoClient("mongo")
db = mongo_client["CSE368"]
user_collection = db['users']
chat_collection = db['chat']

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
        response.set_cookie("user_token", user_token, httponly=False, max_age=3600, samesite=None, secure=False)
        return response
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    user_token = request.cookies.get('user_token')
    if user_token:
        user_collection.update_one({"authentication_token": hashlib.sha256(user_token.encode()).hexdigest()}, {"$unset": {"authentication_token": ""}})
        response = make_response(jsonify(message="Logged out successfully"))
        response.set_cookie('user_token', '', expires=0, httponly=False, samesite=None, secure=False)
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

        user = auth(request)
        texts = chat_collection.find({"username":user}, {"text":1})

        history = ""
        for text in texts:
            history += text["text"].strip() + " "

        print(history, file=sys.stderr)

        chat = model.start_chat(
            history=[
                {"role":"user", "parts": "This starts the chat history; please reference this if someone asks something related to prior knowledge: " + history}
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
        with open('./classes/AICourses.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the AI pathways: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/Courses.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Core Classes: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/ExperientialLearningandResearch.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Experiential Learning and Research pathways: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/HardwareSystemsandNetworkingCourses.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Hardware Systems and Networking pathways: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/Science.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the allowed Science Courses: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/SoftwareCourses.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Software Engineering pathways: {file_contents}")
            print(response.text, file=sys.stderr)
        with open('./classes/TheoryCourses.txt', 'r') as file:
            file_contents = file.read()  # Read the entire file into a single string
            response = chat.send_message(f"Here is the Theory pathways: {file_contents}")
            print(response.text, file=sys.stderr)

        response = chat.send_message("If you have NOT received prior data, say 'Hello! What is your major, and what year are you in?'. Otherwise, say 'Welcome back! What can I do for you?' and use the PRIOR DATA TO INFORM YOUR RESPONSES; They should be concisely and accurate.")
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

    user = auth(request)

    try:
        if user:
            chat_collection.insert_one({"username":user, "text":text}) # add history
        response = chat.send_message(text)
        if response.text:
            return jsonify({"text": response.text}), 200
        else:
            jsonify({"text": "No reply received from Gemini AI."}), 400
    except:
        raise

    # TODO: store user history

def auth(request):
    print(request.cookies, file=sys.stderr)
    user_token = request.cookies.get('user_token')
    if user_token:
        user = user_collection.find_one({"authentication_token": hashlib.sha256(user_token.encode()).hexdigest()})

        if user: # if user exists in database, return username? LOL
            return user["username"]
    
    return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True) #debug=True)
