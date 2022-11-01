# -*- coding: utf-8 -*-
JSON_FILE_PATH = './translation_table.json'
import json

class translator:
    def __init__(self):
        with open(JSON_FILE_PATH, 'r', encoding = 'UTF-8') as loaded_file:
            self.loaded_dict = json.load(loaded_file)
        self.class_Kor = self.loaded_dict["class_trans_kor"]
        self.class_Eng = self.loaded_dict["class_trans_eng"]
        self.engravings_Kor = self.loaded_dict["engraving_trans_kor"]
        self.engravings_Eng = self.loaded_dict["engraving_trans_eng"]

    def get_kor_classname(self, classname):
        try:
            return self.class_Kor[classname]
        except:
            return 'except ' + classname

    def get_eng_classname(self, classname):
        try:
            return self.class_Eng[classname]
        except:
            return 'except ' + classname

    def get_kor_engravings(self, engravings):
        try:
            return self.engravings_Kor[engravings]
        except:
            return 'except ' + engravings
    
    def get_eng_engravings(self, engravings):
        try:
            return self.engravings_Eng[engravings]
        except:
            return 'except ' + engravings

    def translate_classname(self, classname, is_kor = True):
        if is_kor:
            return self.get_kor_classname(classname)
        else:
            return self.get_eng_classname(classname)

    def translate_engravings(self, engravings, is_kor = True):
        if is_kor:
            return self.get_kor_engravings(engravings)
        else:
            return self.get_eng_engravings(engravings)
        
    def get_filename_by_classname(self, classname):
        for k, v in self.class_Kor.items():
            if v == classname:
                print(k)
                return k
    
    def get_filename_by_engravings(self, engravings):
        for k, v in self.engravings_Kor.items():
            if v == engravings:
                print(k)
                return k