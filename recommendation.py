import json
import random
import numpy as np
from utils import get_voices
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

with open('voice_id.json') as f:
    VOICE_ID_DICT = json.load(f)
    
with open('rule_base.json') as f:
    RULE_DICT = json.load(f)

MODEL = SentenceTransformer('paraphrase-MiniLM-L12-v2')

class RuleBase():
    def __init__(self) -> None:
        pass
    
    def pairse_rule(self, data):
        """ 
            Data format
            "genere":  "Self-Help"
            "favor_gender": "male"
            "favor_age": "middle aged"
            "favor_accent": "american"
        """        
        # Get input
        genre = data['genere']
        favor_accent = data['favor_accent']
        favor_age = data['favor_age']
        favor_gender = data['favor_gender']
        rem_voice = None
        for rule_set in RULE_DICT:
            if  genre in rule_set['genere'] and \
                favor_accent in rule_set['favor_accent'] and \
                favor_age in rule_set['favor_age'] and \
                favor_gender in rule_set['favor_gender']:

                num_voice_settings = len(rule_set['settings'])
                index_voice_settings = random.randint(0, num_voice_settings - 1)   
                rem_voice = rule_set['settings'][index_voice_settings]
                break
        return rem_voice
        
        
class SemanticCompare():
    def __init__(self) -> None:
        pass
    
    def get_embedding(self, sentence):
        embedding = MODEL.encode(sentence)
        return embedding
    
    def get_all_voices_embedding(self):
        voice_ids = get_voices()
        
        for id in voice_ids.keys():
            voice_ids[id]['embedding'] = self.get_embedding(voice_ids[id]['metadata'])
        return voice_ids
         
    def compare(self, book_info, voices_id):
        cose = {}
        for key in voices_id.keys():
            vector1 = voices_id[key]['embedding'].reshape(1, -1)
            vector2 = book_info.reshape(1, -1)

            # Calculate cosine similarity between the two vectors
            similarity = cosine_similarity(vector1, vector2)

            cose[key] = float(similarity) #cosine_similarity(voices_id[key]['embedding'], example1)
        
        sorted_dict_descending = sorted(cose.items(), key=lambda item: item[1], reverse=True)
        ids = [voices_id[sorted_dict_descending[0][0]]['metadata'], 
               voices_id[sorted_dict_descending[1][0]]['metadata'], 
               voices_id[sorted_dict_descending[2][0]]['metadata']]
        
        return ids, [sorted_dict_descending[0][0], sorted_dict_descending[1][0], sorted_dict_descending[2][0]]

class RecommandationSystem():
    def __init__(self) -> None:
        pass