# -*- coding: utf-8 -*-
import os
import sys
import json

PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PATH)

from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.static.character_layer import CharacterLayer
from src.layers.utils import CharacterFactory
from src.layers.static.constants import ENGRAVINGS, ARTIFACT_TABLE

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class lostark_sim():
    def __init__(self):
      if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        self.characters_root_path = resource_path('./db/characters/')
        self.skills_root_path = resource_path('./db/skills/')
      else:
        self.characters_root_path = './db/characters/'
        self.skills_root_path = './db/skills/'
      self.character_file_names = os.listdir(self.characters_root_path)
      self.skill_file_names = os.listdir(self.skills_root_path)

    def get_character_file_names(self):
        return self.character_file_names
    
    def get_skill_file_names(self):
        return self.skill_file_names

    def get_one_character_name(self, character_file_name):
        file_path = self.characters_root_path + character_file_name
        with open(file_path, 'r', encoding='UTF-8') as load_file:
            load_json = json.load(load_file)
            return load_json["character_settings"][0]["class_name"]
    
    def get_class_from_skillset(self, skillset_file_name):
        file_path = self.skills_root_path + skillset_file_name
        with open(file_path, 'r', encoding='UTF-8') as load_file:
            load_json = json.load(load_file)
            return load_json["class_name"]

    #def get_character_configs(self, character_file_name):
    #    character_configs = import_character(characters_root_path + character_file_name)
    #    return character_configs

    def get_character_dict(self, character_dict):
        character_factory = CharacterFactory(**character_dict)
        return character_factory.build_dict()

    def get_artifacts(self):
        return list(ARTIFACT_TABLE.keys())

    def get_engravings(self):
        return list(ENGRAVINGS.keys())

    def run_simulator(self, character_json):
        for setting in character_json['character_settings']:
            self.simulator = DpmSimulator(self.get_character_dict(setting), verbose=False)
            self.simulator.run_simulation()
        return True

    def print_simulation_result(self):
        self.simulator.print_result()
        self.simulator.print_damage_details()
        self.simulator.print_delay_statistics()
        self.simulator.print_nuking_cycle()

    def get_DPS_results(self):
        return self.simulator.get_result()
