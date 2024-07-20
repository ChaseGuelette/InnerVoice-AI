
#Note: Inside of linux the system cant detect all of the sound devices for some reason. I should look into that
import pyaudio

def list_audio_devices():
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']} (Input Channels: {info['maxInputChannels']})")
    audio.terminate()

list_audio_devices()
