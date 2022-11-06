# -*- coding: utf-8 -*-
import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5 import uic

from SettingWindow import SettingWindowClass

if __name__ == "__main__" :  
    app = QApplication(sys.argv) 

    myWindow = SettingWindowClass()

    myWindow.show()

    app.exec_()