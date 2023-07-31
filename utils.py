import os
import requests

ELEVEN_LAB_URL = "https://api.elevenlabs.io/v1/"

def write_audio_file(audio: bytes, file_path: str):
    with open(file_path, "wb") as f:
        f.write(audio)
        
def generate_speech_11lab(voice_settings, voice_id, file_path):
    headers = {
        'Content-Type': 'application/json',
        'xi-api-key': os.environ['ELEVEN_LAB_KEY']
    }
    if voice_id is not None:
        url = ELEVEN_LAB_URL + 'text-to-speech/' + voice_id +'?optimize_streaming_latency=0'
    else:
        url = ELEVEN_LAB_URL + 'text-to-speech/'

    response = requests.post(url, json=voice_settings, headers=headers)

    if response.status_code == 200:
        write_audio_file(response.content, file_path)
        return "Request successful."
    else:
        return f"Request failed with status code {response.status_code}."
    
def get_voices():
    headers = {
        'Content-Type': 'application/json',
        'xi-api-key': os.environ['ELEVEN_LAB_KEY']
    }
    url = ELEVEN_LAB_URL + 'voices'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Request successful.")
    else:
        print(f"Request failed with status code {response.status_code}.")
        
    voices = response.json()
    
    voices_id = {}
    for voice in voices['voices']:
        name = voice['name']
        labels = voice['labels']
        
        try:
            accent = labels['accent']
        except:
            accent = labels['accent ']
        
        try:
            description = labels['description']
        except:
            try:
                description = labels['description ']
            except:
                description = ''
    
        age = labels['age']
        gender = labels['gender']
        voice_data = name + ' ' + accent + ' ' + description + ' ' + age + ' ' + gender
        voices_id[voice['voice_id']] = {}
        voices_id[voice['voice_id']]['metadata'] = voice_data

    return voices_id    
    
