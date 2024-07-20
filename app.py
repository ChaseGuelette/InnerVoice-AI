from flask import Flask, request, render_template, jsonify
import responseGenerator

# Initialize OpenAI text generation on app startup
responseGenerator.initOpenAITextGeneration()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.form['inputText']
    input_emotions = request.form['inputEmotions']
    response_text = responseGenerator.generateMP3ForInput(input_text, input_emotions)
    return jsonify({"responseText": response_text})

if __name__ == '__main__':
    app.run()