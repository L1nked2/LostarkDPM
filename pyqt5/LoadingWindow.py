# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic

ui_path = os.path.dirname(os.path.abspath(__file__))
loading_form_class = uic.loadUiType(os.path.join(ui_path, "loading.ui"))[0]

class LoadingWindowClass(QDialog, loading_form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.state_LB.setBold(True)
        self.cancel_Btn.setAlignment(Qt.AlignCenter)
