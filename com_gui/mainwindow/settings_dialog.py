# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable, Optional, Any

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFileDialog

from com_gui.settings import settings
from com_gui.utils.modal_dialog import create_dialog, ModalDialog


def settings_dialog(parent: QWidget):
    def content(dialog: ModalDialog, result_callback: Callable[[Optional[Any]], None]):
        credential_file = QLabel(settings.google_spread_sheet.credential_file)
        open_credential_file = QPushButton("Открыть файл credential.json")

        def open_credential_file_click():
            file_name, filter = QFileDialog.getOpenFileName(dialog, "Открой файл credential.json")
            if not file_name:
                return

            credential_file.setText(file_name)
            settings.google_spread_sheet.credential_file = file_name
            settings.save()

        open_credential_file.clicked.connect(open_credential_file_click)  # type: ignore

        spread_sheet_id = QLineEdit(settings.google_spread_sheet.spread_sheet_id)
        spread_sheet_id.setPlaceholderText("Enter spread sheet id")

        def spread_sheet_id_changed():
            settings.google_spread_sheet.spread_sheet_id = spread_sheet_id.text()
            settings.save()

        spread_sheet_id.textChanged.connect(spread_sheet_id_changed)  # type: ignore

        return [[credential_file, open_credential_file], spread_sheet_id]

    return create_dialog("Settings", parent, settings.modal_dialogs_settings, content)
