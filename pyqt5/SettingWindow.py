# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic


from ResultWindow import ResultWindowClass
from lostark_sim import lostark_sim
from translator import translator

CHARACTER_SETTING_FILEPATH = '../DB/character_settings.json'
ui_path = os.path.dirname(os.path.abspath(__file__))
setting_form_class = uic.loadUiType(os.path.join(ui_path, "setting_window.ui"))[0]

MAX_STAT_SUM = 2200

class SettingWindowClass(QDialog, setting_form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedHeight(254)
        self.setWindowModality(0)

        self.lostark_sim = lostark_sim()
        self.translator = translator()
        self.flag = False
        self.engraving_flag = False
        #self.remain_stat = MAX_STAT_SUM
        self.is_kor = True

        with open(CHARACTER_SETTING_FILEPATH, 'r') as load_file:
            self.loaded_data = json.load(load_file)
        self.character_setting_keys = list(self.loaded_data['character_settings'][0].keys())

        self.result_dict = dict()

        self.init()

        #Element function allocating
        self.buttonBox.accepted.connect(self.accepted) # Forced window closs
        self.buttonBox.rejected.connect(self.rejected)
        self.clear_Btn.clicked.connect(self.accepted)
        self.add_Btn.clicked.connect(self.open_new_setting_window)

        self.class_CB.currentIndexChanged.connect(self.class_selected_func)
        self.artifact_CB.currentIndexChanged.connect(self.artifact_selected_func)
        self.engraving_CB1.currentIndexChanged.connect(lambda: self.engraving_selected_func('1'))
        self.engraving_CB2.currentIndexChanged.connect(lambda: self.engraving_selected_func('2'))
        self.engraving_CB3.currentIndexChanged.connect(lambda: self.engraving_selected_func('3'))
        self.engraving_CB4.currentIndexChanged.connect(lambda: self.engraving_selected_func('4'))
        self.engraving_CB5.currentIndexChanged.connect(lambda: self.engraving_selected_func('5'))
        self.engraving_CB6.currentIndexChanged.connect(lambda: self.engraving_selected_func('6'))
        self.stat_SB2.valueChanged.connect(lambda: self.stat_changed_func('2'))
        self.stat_SB3.valueChanged.connect(lambda: self.stat_changed_func('3'))
        self.stat_SB4.valueChanged.connect(lambda: self.stat_changed_func('4'))

    def set_elements_enable(self, bool):
        self.artifact_CB.setEnabled(bool)
        for i in range(4):
            getattr(self, 'stat_SB'+str(i+1)).setEnabled(bool)
        for j in range(6):
            getattr(self, 'engraving_CB'+str(j+1)).setEnabled(bool)

    def class_selected_func(self):
        if self.class_CB.currentIndex() == 0:
            self.flag = False
            #self.set_elements_enable(False)
            self.clear_elements()
        else:
            self.flag = True
            print(f"{self.class_CB.currentText()} class has selected")
            self.set_elements_enable(True)
            self.update_artifact_CB()
            self.update_engraving_CB()    
            self.init_stat_SB()

    def artifact_selected_func(self):
        selected_index = self.artifact_CB.currentIndex()
        if selected_index == 0:
            self.flag = False
        else:
            self.flag = True
            print(f"{self.artifact_CB.currentText()} artifact has selected")

    def engraving_selected_func(self, index):
        selected_index = getattr(self, 'engraving_CB'+index).currentIndex()
        if selected_index == 0:
            return True
        else:
            self.update_engraving_CB()
            print(f"{getattr(self, 'engraving_CB'+index).currentText()} engraving has selected as engraving "+index)
      
    def stat_changed_func(self, changed_index):
        remains = self.update_remain_stat()
        index_list = ['2', '3', '4']
        for index in index_list:
            getattr(self, 'stat_SB'+index).setRange(0, remains + self.get_stat_SB_value(index))

    def generate_class_CB(self):
        self.class_CB.addItem("Choose class")
        classnames = self.lostark_sim.get_character_file_names()
        for classname in classnames:
            classname = classname[10:]
            self.class_CB.addItem(self.translator.translate_classname(classname, self.is_kor))
            
    def generate_artifact_CB(self):
        self.artifact_CB.addItem("Choose artifact")
        self.flag = False
        artifacts = self.lostark_sim.get_artifacts()
        for artifact in artifacts:
            self.artifact_CB.addItem(artifact)

    def generate_engraving_CB(self):
        self.engraving_flag = True
        engravings = self.lostark_sim.get_engravings()
        for i in range(6):
            getattr(self, 'engraving_CB'+str(i+1)).addItem("Choose engraving")
            for engraving in engravings:
                getattr(self, 'engraving_CB'+str(i+1)).addItem(self.translator.translate_engravings(engraving, self.is_kor))

    def init_stat_SB(self):
        self.stat_SB1.setRange(0, 25)
        self.stat_SB1.setValue(25)
        for i in range(3):
            temp_attr = getattr(self, 'stat_SB'+str(i+2))
            temp_attr.setRange(0, MAX_STAT_SUM)
            temp_attr.setValue(0)
        self.remain_stat_L.setText("Remaining Stat: 2200pt")

    def update_artifact_CB(self):
        if self.artifact_CB.count():
            return True
        else:
            self.generate_artifact_CB()

    def update_engraving_CB(self, index = 0):
        if self.engraving_flag:
            return True
        else:
            self.generate_engraving_CB()

    def update_remain_stat(self):
        remain = MAX_STAT_SUM
        for i in range(3):
            remain -= self.get_stat_SB_value(i+2)
        self.remain_stat_L.setText(f"Remaining Stat: {remain}pt")
        return remain

    def get_stat_SB_value(self, index):
        return getattr(self, 'stat_SB'+str(index)).value()

    def get_current_engravings_list(self):
        current_engravings = []
        for i in range(6):
            if getattr(self, 'engraving_CB'+str(i+1)).currentIndex() != 0:
                engraving_name = self.translator.get_filename_by_engravings(getattr(self, 'engraving_CB'+str(i+1)).currentText())
                current_engravings.append(engraving_name)
        return current_engravings

    def clear_elements(self):
        self.artifact_CB.clear()
        for i in range(6):
            getattr(self, 'engraving_CB'+str(i+1)).clear()
        self.engraving_flag = False
        self.init_stat_SB()
        print("element clear")
        
    def init(self):
        self.class_CB.clear()
        self.clear_elements()
        self.set_elements_enable(False)
        self.generate_class_CB()
        
    def accepted(self):
        if self.flag:
            character_filename = self.translator.get_filename_by_classname(self.class_CB.currentText())
            skill_set_path = f"../db/skills/{character_filename}"
            self.add_character_setting(self.character_setting_keys[0], self.lostark_sim.get_one_character_name(f"character_{character_filename}"))
            for i in range(4):
                self.add_character_setting(self.character_setting_keys[i+1], getattr(self, 'stat_SB'+str(i+1)).value())
            self.add_character_setting(self.character_setting_keys[5], self.get_current_engravings_list())
            #self.add_character_setting(self.character_setting_keys[6], None)
            self.add_character_setting(self.character_setting_keys[7], self.artifact_CB.currentText())
            self.add_character_setting(self.character_setting_keys[8],skill_set_path)

            self.result_json = dict()
            temp = []
            temp.append(self.result_dict)
            self.result_json.setdefault('character_settings', temp)
            self.test()
            self.lostark_sim.run_simulator(self.result_json)
            print("accepted")
            self.open_result_window()
        else:
            print("fail")

    def rejected(self):
        print("rejected")

    def add_character_setting(self, key, value):
        try:
            if type(self.result_dict[key]) is list:
                self.result_dict[key].append(value)
            else:
                self.result_dict[key] = value
        except:
            if key == "options" or key == "artifact_set":
                temp_value = []
                temp_value.append(value)
                self.result_dict.setdefault(key, temp_value)
            else:
                self.result_dict.setdefault(key, value)

    def open_result_window(self):
        # self.hide()
        result_window = ResultWindowClass(self.lostark_sim)
        result_window.is_display = True
        result_window.show()
        while not result_window.is_display:
            print('result_window running')
        # self.init()
        # self.show()

    def test(self):
        file_path = "./saved_json.json"
        with open(file_path, 'w', encoding='UTF-8') as makefile:
            json.dump(self.result_json, makefile, indent = '\t')
            
    def open_new_setting_window(self):
        new_window = SettingWindowClass()
        new_window.show()