
import importlib
import json
import warnings
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill

class SkillsManager:

    def __init__(self, character: CharacterLayer, **kwargs):
        skill_info = json.load(open(character.skill_set, "r", encoding='utf-8'))
        class_name = skill_info['class_name']
        if character.class_name != class_name:
            warnings.warn("Class of character and skill_set does not match", UserWarning)
        #TODO: import identity
        self.policy = skill_info['policy']
        # import skills
        self.skill_pool = list()
        for naive_skill in skill_info['skill_preset']:
            self.skill_pool.append(Skill(**naive_skill))
        
        print('##### Done Initialization of SkillsManager #####')
    
    def get_next_skill(self):
        pass

    def print_skills(self):
        print('skills: (', end='')
        for skill in self.skill_pool[:-1]:
            print(skill, end=', ')
        print(self.skill_pool[-1], end='')
        print(')')
