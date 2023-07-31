import os
import json
import requests
import streamlit as st
from utils import write_audio_file, generate_speech_11lab
from recommendation import *

ELEVEN_LAB_URL = "https://api.elevenlabs.io/v1/text-to-speech/"

# importing required modules
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def get_metadata(input):
    #  metadata:{genre, title, author, description/summary} 
    #  user_data:{nationality, gender, age, voice favor in history, accent}
    st.title("Book's metadata")
    option = st.selectbox(
            'Select the example:',
            ('<select>', 'book1', 'book2', 'book3'))
    
    if option == 'book1':
        input['genre'] = 'Adventure'
        input['title'] = 'The Adventures of Tom Sawyer'
        input['author']= 'Mark Twain'
        input['description'] = 'A classic tale of a young boy named Tom Sawyer and his adventures along the Mississippi River.'

    elif option == 'book2':
        input['genre'] = 'Adventure'
        input['title'] = 'The Adventures of Tom Sawyer'
        input['author'] = 'Mark Twain'
        input['description'] = 'A classic tale of a young boy named Tom Sawyer and his adventures along the Mississippi River.'
        
    elif option == 'book3':
        input['genre'] = 'Adventure'
        input['title'] = 'The Adventures of Tom Sawyer'
        input['author'] = 'Mark Twain'
        input['description'] = 'A classic tale of a young boy named Tom Sawyer and his adventures along the Mississippi River.'
    return input

def get_user(input):
    # user_data:{nationality, gender, age, voice favor in history, accent}

    st.title("User's metadata")
    option = st.selectbox(
            'Select the example:',
            ('<select>', 'user1', 'user2', 'user3'))
    if option == 'user1':
        input['nationality'] = 'Bristish'
        input['gender'] = 'male'
        input['age'] = '25'
        input['voice favor in history'] = 'male'
        input['accent'] = 'Bristish'
        
    elif option == 'user2':
        input['nationality'] = 'American'
        input['gender'] = 'female'
        input['age'] = '50'
        input['voice favor in history'] =  'female'
        input['accent']= 'Bristish'

    elif option == 'user3':
        input['nationality'] = 'Indian'
        input['gender'] = 'female'
        input['age'] = '15'
        input['voice favor in history'] = 'female'
        input['accent'] = 'American'
    return input

    
def select_settings_by_rulebase(level_rule, data):
    """
        This is a baseline version for voice-settings recommendation to generate audiobooks
    """
    # Level1: Rulebase
    if level_rule == 1:
        suggetor = RuleBase()
        data = suggetor.pairse_rule(data)
    # Level2: Semantic Similarity
    elif level_rule == 2:
        st.write(
            "under construction"
        )
    # Level3: Recommendation system
    elif level_rule == 3:
        st.write(
            "under construction"
        )

    return data


def main():
    examples = [
        {
            "title": "The Subtle Art of Not Giving a Fuck A Counterintuitive Approach to Living a Good Life _Mark Manson",
            "genere": "Self-Help",
            "favor_gender": "male",
            "favor_age": "middle age",
            "favor_accent": "bristish",
            "file_path": "data/The Subtle Art of Not Giving a Fuck A Counterintuitive Approach to Living a Good Life _Mark Manson.txt"
        },
        {
            "title": "The Summer I Turned Pretty",
            "genere": "Romance",
            "favor_gender": "female",
            "favor_age": "young",
            "favor_accent": "bristish",
            "file_path": "data/The Summer I Turned Pretty_Jenny Han.txt"
        },
        {
            "title": "Greenlights",
            "genere": "Autobiography",
            "favor_gender": "male",
            "favor_age": "old",
            "favor_accent": "american",
            "file_path": "data/Greenlights_Matthew McConaughey.txt"
        }
    ]
    
    # Select example
    st.title("Book's metadata")
    option = st.selectbox(
            'Select the example:',
            ('','example1', 'example2', 'example3'))
    if '1' in option:
        input = examples[0]
    elif '2' in option:
        input = examples[1]
    elif '3' in option:
        input = examples[2]
    else:
        input = None
    
    st.title('system input: ')
    st.write(input)
        
    level_rule = 1
    button_generate = st.button("generate voice settings")
    if button_generate and input != None:
        rem_voice = select_settings_by_rulebase(level_rule, input)
        st.title('recommend voice setting: ')
        st.write(rem_voice)
        
        voice_id = None
        if rem_voice != None:
            voice_id = rem_voice['voice_id']
        
        text_book = read_text_file(input['file_path'])
        with st.expander("the sample of the book"):
            st.write(text_book)
        voice_settings = {
            "text": text_book,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        
        save_path = 'temp/test_audio.wav'
        with st.spinner("Waiting for the audio book"):
            ret = generate_speech_11lab(voice_settings, voice_id, save_path)
            if 'successful' in ret:
                st.write("The audio generating after suggestion")
                st.audio(save_path)
        
if __name__ == '__main__':
    main()