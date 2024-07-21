import key_points
import signal
from flask import Flask, request, render_template, jsonify, session
import responseGenerator
import audio_capture
import voice_expression
from save_login import login
import openai
import os
from werkzeug.serving import run_simple
import atexit
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
data = {}

@app.route('/')
def index() -> str:
    return render_template('index.html')
    

@app.route('/login', methods=['POST'])
def handle_login() -> str:
    global data
    data = request.json
    username = data.get('username')
    password = data.get('password')
    preferred_name = data.get('preferredName')

    # Call the login function from testSignIn.py
    input_past_context = login(username, password, preferred_name)[-1] or ""

    #input_past_context = "context"
    responseGenerator.initOpenAITextGeneration(preferred_name, input_past_context)

    # Store preferred_name in session
    session['preferred_name'] = preferred_name
    session['username'] = username  # Store username in session for completeness
    session['password'] = password  # Store password in session for completeness
    session['past_context'] = ''  # Initialize past context as empty

    # Simulate a successful login for this example
    return jsonify({"success": True, "message": "Login successful!", "username": username, "preferredName": preferred_name})

@app.route('/logout', methods=['POST'])
def handle_logout() -> str:
    # Clear session data
    add_summary_to_db()
    session.clear()
    return jsonify({"success": True, "message": "Logout successful!"})


def chat_message_to_dict(message):
    if isinstance(message, dict):
        content = message["content"]
        if "User Speach:" in content:
            split_content = content.split("User Speach: ")
            user_speech = split_content[-1]
            content = user_speech.strip()
        else:
            content = content.strip()
        
        return {
            "role": message["role"],
            "content": content
        }
    else:
        content = message.content
        if "User Speach:" in content:
            split_content = content.split("User Speach: ")
            user_speech = split_content[-1]
            content = user_speech.strip()
        else:
            content = content.strip()
        
        return {
            "role": message.role,
            "content": content
        }
    
        

@app.route('/chat-history', methods=['GET'])
def get_chat_history() -> str:
    print("Getting chat history...")
    # Convert each ChatCompletionMessage object to a dictionary
    chat_history = [chat_message_to_dict(message) for message in responseGenerator.conversation]

    # Return the chat history as a JSON response
    return jsonify({"conversation": chat_history})

@app.route('/upload-audio', methods=['POST'])
def upload_audio() -> str:
    if 'audio' not in request.files:
        return jsonify({"success": False, "message": "No audio file part"})

    file = request.files['audio']

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})

    if file:
        filename = 'voice_input.mp3'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Check if file is saved correctly
        try:
            file.save(filepath)
            if os.path.getsize(filepath) > 0:
                return jsonify({"success": True, "message": "Audio uploaded successfully"})
            else:
                os.remove(filepath)
                return jsonify({"success": False, "message": "Empty file uploaded"})
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            return jsonify({"success": False, "message": "Failed to save audio file"})
    
    return jsonify({"success": False, "message": "Invalid file format"})

@app.route('/start-recording', methods=['GET'])
def start_recording() -> str:
    try:
        audio_capture.full_audio_capture()
        output = voice_expression.find_voice_expression()
        
        response_text = responseGenerator.generateMP3ForInput(output[0], output[1])

        # Return the file path of the generated MP3 file
        return jsonify({"responseText": response_text, "audioFile": "/static/output.mp3"})
    except Exception as e:
        print(f"An error occurred while capturing audio: {e}")
        return jsonify({"success": False, "message": "Failed to capture audio"})

def add_summary_to_db():

    print("App is closing")
    global data
    username = data.get('username')
    password = data.get('password')
    preferred_name = data.get('preferredName')
    json_path = "testing-project-2f261-firebase-adminsdk-boek8-6945570a63.json"

    database = db.reference()

    print(responseGenerator.conversation)
    #conversation = [{"role":"user", "content": "Emotions : Joy Amusement Disappointment Shame Distress Fear Pain Sadness \nUser Speach: my dog died and i fell down the stairs"}, {"role":"assistant", "content": "it is really interesting that you say that you should probably lock in and work harder"}]
    summary = key_points.key_points_extraction(openai.api_key, responseGenerator.conversation)


    # Retrieve the existing list of summaries
    existing_summaries = database.child("Users").child(username).child("Summaries").get() or []
    # Append the new summary to the list
    existing_summaries.append(summary)
    # Write the updated list back to the database
    database.child("Users").child(username).child("Summaries").set(existing_summaries)

atexit.register(add_summary_to_db)

if __name__ == '__main__':
    run_simple('localhost', 5000, app, use_reloader=False, use_debugger=True, use_evalex=True)
    