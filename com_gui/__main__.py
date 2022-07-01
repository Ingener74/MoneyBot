# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

from com_gui.mainwindow.main_window import MainWindow
from com_gui.settings import settings

app = QApplication()

settings.modal_dialogs_settings.save_callback = lambda: settings.save()

main_window = MainWindow()
main_window.show()

sys.exit(app.exec())
