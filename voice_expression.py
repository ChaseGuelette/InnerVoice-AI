import os

from utilities import print_emotions

from hume import HumeBatchClient
from hume.models.config import BurstConfig, ProsodyConfig

def find_voice_expression():

    client = HumeBatchClient(open(os.path.join(os.path.dirname(__file__), 'hume-key.txt'), 'r').read().strip())

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path to the MP3 file
    mp3_file_path = os.path.join(script_dir, "audio-files", "speach.mp3")


    urls = ["https://storage.googleapis.com/hume-test-data/audio/ninth-century-laugh.mp3"]
    burst_config = BurstConfig()
    prosody_config = ProsodyConfig()

    # Use a webhook callback to get a POST notification to your API when the batch job has completed
    callback_url = "https://mockbin.org/bin/08d1f920-801c-4de1-9622-8c7b39658009"
    job = client.submit_job(urls=[], configs=[burst_config, prosody_config], files=[mp3_file_path], callback_url=callback_url)
    #job = client.submit_job([mp3_file_path], [burst_config, prosody_config])

    print("Running...", job)
    job.await_complete()
    print("Job completed with status: ", job.get_status())

    full_predictions = job.get_predictions()
    print(full_predictions)
    for source in full_predictions:
        # print(str(source))
        # source_name = source["source"]["filename"]
        predictions = source["results"]["predictions"]

        for prediction in predictions:
            print()
            print("Speech prosody")
            prosody_predictions = prediction["models"]["prosody"]["grouped_predictions"]
            for prosody_prediction in prosody_predictions:
                for segment in prosody_prediction["predictions"][:1]:
                    return print_emotions(segment["emotions"])

            # print()
            # print("Vocal burst")
            # burst_predictions = prediction["models"]["burst"]["grouped_predictions"]
            # for burst_prediction in burst_predictions:
            #     for segment in burst_prediction["predictions"][:1]:
            #         print_emotions(segment["emotions"])