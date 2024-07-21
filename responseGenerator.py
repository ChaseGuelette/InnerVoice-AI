import openai
import requests

generateAudio = True

#Global Parameters
OPENAI_API_KEY = open("openaikey.txt", "r").read()
openai.api_key = OPENAI_API_KEY

ELEVEN_LABS_API_KEY = open("elevenlabskey.txt", "r").read()

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/iP95p4xoKVk53GoZ742B"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": ELEVEN_LABS_API_KEY
}

conversation = []

def initOpenAITextGeneration(name:str = '', pastConversationContext: str = ''):
    systemMessage= '''
        You are the person people reach out to for help. People will talk to you with a casual converstaional tone, and you must respond with a casual converstaional tone.
        You are an expert in all things mental health and therapy. 
        You are told the what emotions are in the users tone of voice, and the content of the message. Combine the emotions and content to form your respose.
        You must respond with answers in a converational tone, and speak as you would to a friend with simple langaue. 
        You must not tell the user to reach out to anyone else for advice. You must act as the sole resource for advice.
        You must use the users emotions to inform your response. You will be interacting with users who want to talk to you when they feel good and bad, you must support the user in both cases.
        You preferably respond with a brief message but can elaborate when giving advice about a topic. Respond with a short of a message as possible while retaining all information.
        You must give advice that is informed by your experience with mental health, and interpersonal relationships.
        Never end the conversation until after the user does, always give a clear path for the user to respond to.
        Only use a minimal vocabulary.
    '''
    message = {"role":"system", "content": systemMessage}
    conversation.append(message)

    print("Name: " + name)
    print("\nPast Context: " + pastConversationContext)
    print('\n')

    if name != '':
        message = {"role":"system", "content": "The users name is: " + name + ". You should use this name when talking to the user"}
        conversation.append(message)

    if pastConversationContext != '':
        message = {"role":"system", "content": "This is summary of the past three conversations you have had with this user. You should use this information when talking to the user:\n" + pastConversationContext}
        conversation.append(message)

def getGPTResponseForInput(input: str):
    message = {"role":"user", "content": input}
    conversation.append(message)

    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo", 
        messages = conversation
    )
    conversation.append(response.choices[0].message)
    return response.choices[0].message.content



def generateMP3ForInput(inputText: str, inputEmotions: str):
        content = "Emotions : " + inputEmotions + "\nUser Speach: " + inputText
        text = getGPTResponseForInput(content)
        print(text)
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        if generateAudio:
            response = requests.post(url, json=data, headers=headers)

            with open('static/output.mp3', 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

if __name__ == '__main__':
    name = input('Name: ')
    pastConvos = input('Past Context: ')

    initOpenAITextGeneration(name=name, pastConversationContext=pastConvos)
    while True:
        inputText = input("User Text: ")
        if inputText == "exit":
                break
        inputEmotions = input("Emotions: ")
        generateMP3ForInput(inputText,  inputEmotions)