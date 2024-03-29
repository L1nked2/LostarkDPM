# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic


from .ResultWindow import ResultWindowClass
from .lostark_sim import lostark_sim
from .translator import translator

UI_FILENAME = 'setting_window_alpha.ui'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
  CHARACTER_SETTING_FILEPATH = resource_path('./db/character_settings.json')
  ui_path = resource_path(UI_FILENAME)
else:
  CHARACTER_SETTING_FILEPATH = './db/character_settings.json'
  ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), UI_FILENAME)

setting_form_class = uic.loadUiType(ui_path)[0]

MAX_STAT_SUM = 2200

class SettingWindowClass(QDialog, setting_form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedHeight(220)
        self.setWindowModality(0)

        self.lostark_sim = lostark_sim()
        self.translator = translator()
        self.flag = False
        self.engraving_flag = False
        #self.remain_stat = MAX_STAT_SUM
        self.is_kor = True

        with open(CHARACTER_SETTING_FILEPATH, 'r', encoding='utf-8') as load_file:
            self.loaded_data = json.load(load_file)
        self.character_setting_keys = list(self.loaded_data['character_settings'][0].keys())

        self.result_dict = dict()

        self.set_widget_size()
        self.allocate_function()
        self.init()

    def set_elements_enable(self, bool):
        self.artifact_CB.setEnabled(bool)
        for i in range(4):
            getattr(self, 'stat_SB'+str(i+1)).setEnabled(bool)
        for j in range(10):
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
        classnames = self.lostark_sim.get_skill_file_names()
        for classname in classnames:
            new_classname = self.translator.translate_classname(classname, self.is_kor)
            if new_classname:
                self.class_CB.addItem(new_classname)
            else:
                self.class_CB.addItem(classname)
                continue
            
    def generate_artifact_CB(self):
        self.artifact_CB.addItem("Choose artifact")
        self.flag = False
        artifacts = self.lostark_sim.get_artifacts()
        for artifact in artifacts:
            new_artifactname = self.translator.translate_artifact(artifact, self.is_kor)
            if new_artifactname:
                self.artifact_CB.addItem(new_artifactname)
            else:
                self.artifact_CB.addItem(artifact)
                continue

    def generate_engraving_CB(self):
        self.engraving_flag = True
        engravings = self.lostark_sim.get_engravings()
        for i in range(10):
            getattr(self, 'engraving_CB'+str(i+1)).addItem("Choose engraving")
            for engraving in engravings:
                new_engraving = self.translator.translate_engravings(engraving, self.is_kor)
                if new_engraving:
                    getattr(self, 'engraving_CB'+str(i+1)).addItem(new_engraving)
                else:
                    continue

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
        for i in range(10):
            if getattr(self, 'engraving_CB'+str(i+1)).currentIndex() != 0:
                engraving_name = self.translator.get_filename_by_engravings(getattr(self, 'engraving_CB'+str(i+1)).currentText(), self.is_kor)
                current_engravings.append(engraving_name)
        return current_engravings

    def clear_elements(self):
        self.artifact_CB.clear()
        for i in range(10):
            getattr(self, 'engraving_CB'+str(i+1)).clear()
        self.engraving_flag = False
        self.init_stat_SB()
        print("element clear")
        
    def init(self):
        self.result_dict = dict()
        self.class_CB.clear()
        self.clear_elements()
        self.set_elements_enable(False)
        self.generate_class_CB()
        
    def accepted(self):
        if self.flag:
            skillset_filename = self.translator.get_filename_by_classname(self.class_CB.currentText(), self.is_kor)
            skill_set_path = f"./db/skills/{skillset_filename}"
            self.add_character_setting(self.character_setting_keys[0], self.lostark_sim.get_class_from_skillset(skillset_filename))
            for i in range(4):
                self.add_character_setting(self.character_setting_keys[i+1], getattr(self, 'stat_SB'+str(i+1)).value())
            self.add_character_setting(self.character_setting_keys[5], self.get_current_engravings_list())
            #self.add_character_setting(self.character_setting_keys[6], None)
            artifact_name = self.translator.get_filename_by_artifact(self.artifact_CB.currentText(), self.is_kor)
            self.add_character_setting(self.character_setting_keys[7], artifact_name)
            self.add_character_setting(self.character_setting_keys[8], skill_set_path)

            self.result_json = dict()
            temp = []
            temp.append(self.result_dict)
            self.result_json.setdefault('character_settings', temp)
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
        self.hide()
        result_window = ResultWindowClass(self.lostark_sim, self.is_kor)
        result_window.is_display = True
        result_window.exec()
        self.init()
        self.show()
            
    def open_new_setting_window(self):
        new_window = SettingWindowClass()
        new_window.show()
        
    def translate(self):
        self.is_kor = not self.is_kor
        label = self.translator.get_label_keys(self.is_kor)
        for i in range(8):
            getattr(self, 'LB_' + str(i+1)).setText(self.translator.translate_label(label[i], self.is_kor))
        self.clear_Btn.setText(self.translator.translate_label(label[8], self.is_kor))
        self.translate_Btn.setText(self.translator.translate_label(label[9], self.is_kor))
        self.buttonBox.button(self.buttonBox.Ok).setText(self.translator.translate_label(label[10], self.is_kor))
        self.buttonBox.button(self.buttonBox.Cancel).setText(self.translator.translate_label(label[11], self.is_kor))
        self.init()
        
    def allocate_function(self):
        #Widget function allocating
        self.buttonBox.accepted.connect(self.accepted) # Forced window closs
        self.buttonBox.rejected.connect(self.rejected)
        self.clear_Btn.clicked.connect(self.init)
        self.translate_Btn.clicked.connect(self.translate)

        self.class_CB.currentIndexChanged.connect(self.class_selected_func)
        self.artifact_CB.currentIndexChanged.connect(self.artifact_selected_func)
        self.engraving_CB1.currentIndexChanged.connect(lambda: self.engraving_selected_func('1'))
        self.engraving_CB2.currentIndexChanged.connect(lambda: self.engraving_selected_func('2'))
        self.engraving_CB3.currentIndexChanged.connect(lambda: self.engraving_selected_func('3'))
        self.engraving_CB4.currentIndexChanged.connect(lambda: self.engraving_selected_func('4'))
        self.engraving_CB5.currentIndexChanged.connect(lambda: self.engraving_selected_func('5'))
        self.engraving_CB6.currentIndexChanged.connect(lambda: self.engraving_selected_func('6'))
        self.engraving_CB7.currentIndexChanged.connect(lambda: self.engraving_selected_func('7'))
        self.engraving_CB8.currentIndexChanged.connect(lambda: self.engraving_selected_func('8'))
        self.engraving_CB9.currentIndexChanged.connect(lambda: self.engraving_selected_func('9'))
        self.engraving_CB10.currentIndexChanged.connect(lambda: self.engraving_selected_func('10'))
        
        self.stat_SB2.valueChanged.connect(lambda: self.stat_changed_func('2'))
        self.stat_SB3.valueChanged.connect(lambda: self.stat_changed_func('3'))
        self.stat_SB4.valueChanged.connect(lambda: self.stat_changed_func('4'))
        
    def set_widget_size(self):
        self.class_CB.setFixedSize(400, 21)
        self.artifact_CB.setFixedSize(400, 21)
        self.stat_SB1.setFixedSize(70, 21)
        self.stat_SB2.setFixedSize(70, 21)
        self.stat_SB3.setFixedSize(70, 21)
        self.stat_SB4.setFixedSize(70, 21)
        #self.class_CB.setFixedSize(170, 21)
        #self.artifact_CB.setFixedSize(170, 21)