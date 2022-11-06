# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic

from lostark_sim import lostark_sim

ui_path = os.path.dirname(os.path.abspath(__file__))
result_form_class = uic.loadUiType(os.path.join(ui_path, "result_window_alpha.ui"))[0]


class ResultWindowClass(QDialog, result_form_class) :
    def __init__(self, simulator) :
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setFixedHeight(219)
        self.setWindowModality(0)
        
        self.is_display = False
        
        # self.ok_Btn.clicked.connect(self.close_window)

        self.result_simulator = simulator
        self.result_simulator.print_simulation_result()
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

    def close_window(self):
        self.hide()
        self.is_display = False
        return True
