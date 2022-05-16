# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

from ComGui.MainWindow.MainWindow import MainWindow
from ComGui.Settings import settings

app = QApplication()

settings.modal_dialogs_settings.save_callback = lambda: settings.save()

main_window = MainWindow()
main_window.show()

sys.exit(app.exec())
