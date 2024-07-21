import os
from sys import byteorder
from array import array
from struct import pack

import pyaudio
from pydub import AudioSegment
import wave

THRESHOLD = 1000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
        
    snd_started  = False
    r = array ('h')

    for i in snd_data:
        if not snd_started and abs(i)> THRESHOLD:
            snd_started = True
            r.append(i)

        elif snd_started:
            r.append(i)
    return r

    #snd_data = _trim(snd_data)

def add_silence(snd_data, seconds):
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r

def record():

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False
    
    r = array('h')

    while 1:
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)
        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True
            num_silent = 0

        # Stop recording when 30 consecutive silent chunks are detected
        if snd_started and num_silent > 125:
            break

    
    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    # Create the subfolder if it doesn't exist
    subfolder = "audio-files"
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # Include the subfolder name in the file path
    path = os.path.join(subfolder, path)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close


def full_audio_capture():
    print("please speak a word into the microphone")
    record_to_file('demo.wav')
    print("done - result written to demo.wav")

    # Create the subfolder if it doesn't exist
    subfolder = "audio-files"
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # Include the subfolder name in the input file path
    input_path = os.path.join(subfolder, "demo.wav")

    sound = AudioSegment.from_wav(input_path)

    # Include the subfolder name in the output file path
    output_path = os.path.join(subfolder, "speach.mp3")
    sound.export(output_path, format="mp3")

# if __name__=='__main__':
#     print("please speak a word into the microphone")
#     record_to_file('demo.wav')
#     print("done - result written to demo.wav")

#     # Create the subfolder if it doesn't exist
#     subfolder = "audio-files"
#     if not os.path.exists(subfolder):
#         os.makedirs(subfolder)

#     # Include the subfolder name in the input file path
#     input_path = os.path.join(subfolder, "demo.wav")

#     sound = AudioSegment.from_wav(input_path)

#     # Include the subfolder name in the output file path
#     output_path = os.path.join(subfolder, "output.mp3")
#     sound.export(output_path, format="mp3")