# -*- coding: utf-8 -*-
import os
import sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
JSON_FILE_PATH = resource_path('translation_table.json')
import json

class translator:
    def __init__(self):
        with open(JSON_FILE_PATH, 'r', encoding = 'UTF-8') as loaded_file:
            self.loaded_dict = json.load(loaded_file)
        self.class_Kor = self.loaded_dict["class_trans_kor"]
        self.class_Eng = self.loaded_dict["class_trans_eng"]
        self.engravings_Kor = self.loaded_dict["engraving_trans_kor"]
        self.engravings_Eng = self.loaded_dict["engraving_trans_eng"]
        self.label_Kor = self.loaded_dict["label_trans_kor"]
        self.label_Eng = self.loaded_dict["label_trans_eng"]

    def get_kor_classname(self, classname):
        try:
            return True, self.class_Kor[classname]
        except:
            return False, 'except ' + classname

    def get_eng_classname(self, classname):
        try:
            return True, self.class_Eng[classname]
        except:
            return False, 'except ' + classname

    def get_kor_engravings(self, engravings):
        try:
            return True, self.engravings_Kor[engravings]
        except:
            return False, 'except ' + engravings
    
    def get_eng_engravings(self, engravings):
        try:
            return True, self.engravings_Eng[engravings]
        except:
            return False, 'except ' + engravings
        
    def get_label_keys(self, is_kor):
        if is_kor:
            return list(self.label_Kor.keys())
        else:
            return list(self.label_Eng.keys())

    def translate_classname(self, classname, is_kor = True):
        if is_kor:
            result = self.get_kor_classname(classname)
            if result[0]:
                return result[1]
            else:
                return False
        else:
            result = self.get_eng_classname(classname)
            if result[0]:
                return result[1]
            else:
                return False

    def translate_engravings(self, engravings, is_kor = True):
        if is_kor:
            result = self.get_kor_engravings(engravings)
            if result[0]:
                return result[1]
            else:
                return False
        else:
            result = self.get_eng_engravings(engravings)
            if result[0]:
                return result[1]
            else:
                return False
            
    def translate_label(self, lable, is_kor = True):
        if is_kor:
            return self.label_Kor[lable]
        else:
            return self.label_Eng[lable]
        
    def get_filename_by_classname(self, classname, is_kor = True):
        if is_kor:
            for k, v in self.class_Kor.items():
                if v == classname:
                    print(k)
                    return k
        else:
            for k, v in self.class_Eng.items():
                if v == classname:
                    print(k)
                    return k
    
    def get_filename_by_engravings(self, engravings, is_kor = True):
        if is_kor:
            for k, v in self.engravings_Kor.items():
                if v == engravings:
                    print(k)
                    return k
        else:
            for k, v in self.engravings_Eng.items():
                if v == engravings:
                    print(k)
                    return k