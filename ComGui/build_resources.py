# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import run

if __name__ == '__main__':
    run('pyside6-uic res/MainWindow.ui -o res/Ui_MainWindow.py')
