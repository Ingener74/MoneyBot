# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field, InitVar
from functools import partial
from typing import Any, Callable, Optional, List, Dict

from PySide6.QtCore import QRect, QTimer, Qt
from PySide6.QtGui import QResizeEvent, QMoveEvent
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLayout

from com_gui.utils.settings_utils import ByteArraySetting


@dataclass()
class ModalDialogSettings:
    geometries: Dict[str, ByteArraySetting] = field(default_factory=dict)
    save_callback: InitVar = None


class ModalDialog(QDialog):
    def __init__(self, name: str, parent, settings: ModalDialogSettings):
        super(ModalDialog, self).__init__(parent=parent)
        self.__name = name
        self.__showed = False
        self.settings = settings

    def showEvent(self, _) -> None:
        self.__showed = True
        has_settings_for_modal = self.__name in self.settings.geometries
        if has_settings_for_modal and self.settings.geometries[self.__name].is_valid():
            self.restoreGeometry(self.settings.geometries[self.__name].restore())

    def save_geometry(self):
        def on_timer(geometry: QRect):
            if self.geometry() == geometry:
                if self.__name not in self.settings.geometries:
                    self.settings.geometries[self.__name] = ByteArraySetting()
                self.settings.geometries[self.__name].save(self.saveGeometry())
                if self.settings.save_callback is not None:
                    self.settings.save_callback()

        QTimer.singleShot(100, partial(on_timer, self.geometry()))

    def resizeEvent(self, ev: QResizeEvent) -> None:
        if self.__showed:
            self.save_geometry()

    def moveEvent(self, ev: QMoveEvent) -> None:
        if self.__showed:
            self.save_geometry()


ResultCallback = Callable[[Optional[Any]], None]
Content = Callable[[ModalDialog, ResultCallback], List[QWidget]]


def create_dialog(name: str, parent: QWidget, settings: ModalDialogSettings, content: Content) -> Optional[Any]:
    dialog = ModalDialog(name, parent, settings)
    dialog.setModal(True)
    dialog.setWindowTitle(name)
    dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    dialog.result = None

    layout = QVBoxLayout(dialog)

    def update_result(result: Optional[Any]):
        dialog.result = result
        dialog.accept()

    list_ = content(dialog, update_result)

    for w in list_:
        if isinstance(w, list):
            layout_ = QHBoxLayout()
            for widget_ in w:
                if isinstance(widget_, list):
                    layout_.addWidget(widget_[0], widget_[1])
                else:
                    layout_.addWidget(widget_)
            layout.addLayout(layout_)
        elif isinstance(w, QLayout):
            layout.addLayout(w)
        else:
            layout.addWidget(w)

    r = dialog.exec_()
    if r == QDialog.Accepted and dialog.result is not None:
        return dialog.result
    return None
