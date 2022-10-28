# -*- coding: utf-8 -*-
import os
import sys
import csv
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.static.character_layer import CharacterLayer
from src.layers.utils import CharacterFactory
from src.layers.static.constants import ENGRAVINGS, ARTIFACT_TABLE


class lostark_sim():
    def __init__(self):
        self.characters_root_path = '../db/characters/'
        self.character_file_names = os.listdir(self.characters_root_path)

    def get_character_file_names(self):
        return self.character_file_names

    def get_one_character_name(self, character_file_name):
        file_path = self.characters_root_path + character_file_name
        with open(file_path, 'r', encoding='UTF-8') as load_file:
            load_json = json.load(load_file)
            return load_json["character_settings"][0]["class_name"]

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

    def get_DPS_results(self):
        return self.simulator.get_result()
