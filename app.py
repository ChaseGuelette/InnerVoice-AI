from flask import Flask, request, render_template, jsonify
import responseGenerator
from testSignIn import login

# Initialize OpenAI text generation on app startup
responseGenerator.initOpenAITextGeneration()

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate() -> str:
    input_text = request.form['inputText']
    input_emotions = request.form['inputEmotions']
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

    # Simulate a successful login for this example
    return jsonify({"success": True, "message": "Login successful!", "username": username, "preferredName": preferred_name})

if __name__ == '__main__':
    app.run(debug=True)  # Use debug=True for development purposes