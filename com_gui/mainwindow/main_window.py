# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
from functools import partial
from typing import Optional

from PySide6.QtCore import QRect, QTimer
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from com_gui.mainwindow.settings_dialog import settings_dialog
from com_gui.model.purchase_model import create_model
from com_gui.res.ui_main_window import Ui_MainWindow
from com_gui.settings import settings

from constants import products_config
from money.product import Products


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__showed = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__check: Optional[Products] = None

        self.init_table_view()
        self.init_open_button()
        self.init_send_button()
        self.init_settings_button()

    def showEvent(self, event) -> None:
        self.__showed = True
        self.restoreGeometry(settings.main_window.geometry.restore())

    def resizeEvent(self, _) -> None:
        if self.__showed:
            self.save_geometry()

    def moveEvent(self, _) -> None:
        if self.__showed:
            self.save_geometry()

    def save_geometry(self):
        def on_timer(geometry: QRect):
            if self.geometry() == geometry:
                settings.main_window.geometry.save(self.saveGeometry())
                settings.save()

        QTimer.singleShot(100, partial(on_timer, self.geometry()))

    def init_send_button(self):
        def send():
            if settings.google_spread_sheet.spread_sheet_id == "":
                QMessageBox.warning(self, "Error", "Set spread sheet id in settings")
            if settings.google_spread_sheet.credential_file == "":
                QMessageBox.warning(self, "Error", "Set credential file in settings")
            if not self.__check.goods:
                QMessageBox.warning(self, "Error", "Check empty")
            self.__check.save_to_google_sheet(settings.google_spread_sheet.credential_file,
                                              settings.google_spread_sheet.spread_sheet_id,
                                              products_config)
            QMessageBox.information(self, "Успешно", "Чек сохранён!")

        self.ui.pushButtonSend.clicked.connect(send)
        self.ui.pushButtonSend.setEnabled(False)

    def init_open_button(self):
        def open_file():
            try:
                file_name, filter = QFileDialog.getOpenFileName(self, "Открой файл с данными о коммунальных платежах")
                if not file_name:
                    return

                self.__check = Products.from_communal_payments(file_name)
                self.ui.pushButtonSend.setEnabled(True)
                model = create_model(self.__check)
                self.ui.tableViewPurchases.setModel(model)
            except Exception:
                QMessageBox.warning(self, "Error", traceback.format_exc())

        self.ui.pushButtonOpen.clicked.connect(open_file)

    def init_table_view(self):
        model = create_model(Products())
        self.ui.tableViewPurchases.setModel(model)

        self.ui.tableViewPurchases.horizontalHeader().restoreState(settings.main_window.table.state.restore())

        def section_resized():
            settings.main_window.table.state.save(self.ui.tableViewPurchases.horizontalHeader().saveState())
            settings.save()

        self.ui.tableViewPurchases.horizontalHeader().sectionResized.connect(section_resized)

    def init_settings_button(self):
        def open_settings():
            settings_dialog(self)

        self.ui.pushButtonSettings.clicked.connect(open_settings)
