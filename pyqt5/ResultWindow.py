# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic

from lostark_sim import lostark_sim

ui_path = os.path.dirname(os.path.abspath(__file__))
result_form_class = uic.loadUiType(os.path.join(ui_path, "sample_result.ui"))[0]


class ResultWindowClass(QDialog, result_form_class) :
    def __init__(self, simulator) :
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setFixedHeight(219)

        self.result_simulator = simulator
        self.result_simulator.print_simulation_result()
        self.display_result()
        #self.share_TW.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        def run_simulator(self):
            return True

        def display_result(self):
            dps = '0'
            dps6 = '0'
            dps8 = '0'
            dps10 = '0'

            self.dps_TB.append(dps)
            self.dps6_TB.append(dps6)
            self.dps8_TB.append(dps8)
            self.dps10_TB.append(dps10)
