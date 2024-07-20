from flask import Flask, request, render_template, jsonify, session
import responseGenerator
from testSignIn import login

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route('/')
def index() -> str:
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate() -> str:
    input_past_context = request.form['inputPastContext']
    input_text = request.form['inputText']
    input_emotions = request.form['inputEmotions']
    
    # Retrieve preferred_name from session
    preferred_name = session.get('preferred_name', '')

    # Initialize OpenAI text generation with name and past context
    responseGenerator.initOpenAITextGeneration(preferred_name, input_past_context)
    
    response_text = responseGenerator.generateMP3ForInput(input_text, input_emotions)
    return jsonify({"responseText": response_text})

@app.route('/login', methods=['POST'])
def handle_login() -> str:
    data = request.json
    username = data.get('username')
    password = data.get('password')
    preferred_name = data.get('preferredName')

    # Call the login function from testSignIn.py
    login(username, password)

    # Store preferred_name in session
    session['preferred_name'] = preferred_name

    # Simulate a successful login for this example
    return jsonify({"success": True, "message": "Login successful!", "username": username, "preferredName": preferred_name})

if __name__ == '__main__':
    app.run(debug=True)  # Use debug=True for development purposes