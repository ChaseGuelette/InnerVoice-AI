from typing import Any


def print_emotions(emotions: list[dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    e = ''
    for emotion in ["Adoration","Joy", "Amusement", "Anger", "Awe", "Calmness", "Confusion", "Contempt","Pride", "Contentment", "Craving", "Desire","Love", "Disappointment","Shame", "Distress","Disgust", "Fear", "Interest", "Pain","Sadness"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")
        if emotion_map[emotion] > .1:
            e += emotion + " "
    return e

        
