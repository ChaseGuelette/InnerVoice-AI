import os
from hume import HumeVoiceClient, MicrophoneInterface
from dotenv import load_dotenv
import asyncio

async def main() -> None:
    # Paste your Hume API key here.
    HUME_API_KEY = open("hume-key.txt", "r").read()
    # Connect and authenticate with Hume
    client = HumeVoiceClient(HUME_API_KEY)

    # Start streaming EVI over your device's microphone and speakers
    # async with MicrophoneInterface() as source:
    async with client.connect() as socket:
        await MicrophoneInterface.start(socket)
        #async for response in client.stream(source):
            #print(response)
    

asyncio.run(main())

