# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic

from .lostark_sim import lostark_sim
from .translator import translator

UI_FILENAME = 'result_window_alpha.ui'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
ui_path = resource_path(UI_FILENAME)
result_form_class = uic.loadUiType(ui_path)[0]

class ResultWindowClass(QDialog, result_form_class) :
    def __init__(self, simulator, is_kor) :
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setFixedHeight(155)
        self.setWindowModality(0)
        self.is_kor = is_kor
        self.is_display = False
        
        # self.ok_Btn.clicked.connect(self.close_window)

        self.result_simulator = simulator
        self.transator = translator()
        self.result_simulator.print_simulation_result()
        self.translate()
        self.display_result()

    # def closeEvent(self, event):
    #     self.close_window()
    #     return True

    def run_simulator(self):
        return True

    def display_result(self):
        self.is_display = True
        dps, dps6, dps8, dps10 = list(map(str, self.result_simulator.get_DPS_results()))

        self.dps_TB.append(dps)
        self.dps6_TB.append(dps6)
        self.dps8_TB.append(dps8)
        self.dps10_TB.append(dps10)
        
    def translate(self):
        labels = self.transator.get_label_keys(self.is_kor)
        for i in range(3):
            getattr(self, 'LB_' + str(i+1)).setText(self.transator.translate_label(labels[12+i], self.is_kor))

    def close_window(self):
        self.hide()
        self.is_display = False
        return True
