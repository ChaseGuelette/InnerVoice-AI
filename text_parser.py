import whisper
from pydub import AudioSegment
import numpy as np
from torch import from_numpy 
import warnings
import openai 



def audio_to_numpy(audio):
    # Convert AudioSegment to NumPy array
    samples = np.array(audio.get_array_of_samples())
    # Reshape and normalize if needed (convert from int16 to float32)
    samples = samples.astype(np.float32) / 32768.0
    return samples

def transcribe_mp3(mp3_file_path):
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

    # Load the Whisper model
    model = whisper.load_model("base")

    # Convert MP3 to WAV format
    audio = AudioSegment.from_mp3(mp3_file_path)
    
    # Convert AudioSegment to NumPy array
    audio_np = audio_to_numpy(audio)
    
    # Create a 1D NumPy array from the audio samples
    audio_np = np.array(audio_np)

    # Transpose the NumPy array to match Whisper's expected input shape
    audio_np = torch.from_numpy(audio_np)

    # Transcribe the audio
    result = model.transcribe(audio_np)
    return result['text']

def key_points_extraction(api_key, transcription):
    conversation = []
    message = {"role":"system", "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about. This is the conversation: " + transcription}
    conversation.append(message)
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= conversation
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    audio_file_path = "testing-audio.mp3"
    api_key = open("openaikey.txt", "r").read()
    
    transcription = transcribe_mp3(audio_file_path)
    key_points = key_points_extraction(api_key, transcription)

    print(transcription)
