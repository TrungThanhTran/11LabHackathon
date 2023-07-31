import json
import random
import streamlit as st

with open('voice_id.json') as f:
    VOICE_ID_DICT = json.load(f)
    
with open('rule_base.json') as f:
    RULE_DICT = json.load(f)


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
    
class RecommandationSystem():
    def __init__(self) -> None:
        pass