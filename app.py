from flask import Flask, request, render_template, jsonify, session
import responseGenerator
import audio_capture
import voice_expression
from testSignIn import login
import openai
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route('/')
def index() -> str:
    return render_template('index.html')
    

@app.route('/login', methods=['POST'])
def handle_login() -> str:
    data = request.json
    username = data.get('username')
    password = data.get('password')
    preferred_name = data.get('preferredName')

    # Call the login function from testSignIn.py
    login(username, password)

    input_past_context = ""
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

if __name__ == '__main__':
    app.run(debug=True)  # Use debug=True for development purposes