import openai 
from dotenv import load_dotenv
import os

def key_points_extraction(api_key, conversation):

    conversationAsStr = ""    
    for entry in conversation:
        if isinstance(entry, dict) and entry["role"] == "system":
            continue
        if entry.role == "system":
            continue
        content = entry["content"]
        # check if "User Speech: " is in the string
        if "User Speach:" in content:
            
            # split the string at "User Speech: "
            split_content = content.split("User Speach: ")
            
            # take the second part of the split string
            user_speech = split_content[-1]
            #print("split_content\n\n" + user_speech.strip() + "\n\n")
            # update the dictionary
            conversationAsStr = conversationAsStr + "User Speach:" + user_speech.strip()
        # if "User Speech: " is not in the string, the content is already the user speech
        else:
            #print("content stripe: " + content.strip())
            conversationAsStr = conversationAsStr + "AI therapist response: " + content.strip()

    #print("This is the conversation as a string: \n\n\n" + conversationAsStr + "\n\n\n")
    #"content": "Emotions : Joy Amusement Disappointment Shame Distress Fear Pain Sadness \nUser Speach: It didn't happen"

    if (conversationAsStr == ""): 
        return ""
    message = [{"role":"system", "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about. This is the conversation: " + conversationAsStr}]
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= message
    )
    return response.choices[0].message.content

if __name__ == "__main__":

    load_dotenv()  # Load environment variables from .env file

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

    conversation = [{"content": "Emotions : Joy Amusement Disappointment Shame Distress Fear Pain Sadness \nUser Speach: my dog died and i fell down the stairs"}, {"content": "it is really interesting that you say that you should probably lock in and work harder"}]
    key_points = key_points_extraction(openai.api_key, conversation)

    print(key_points)