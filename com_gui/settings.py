# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from traceback import format_exc

from dacite import from_dict
from loguru import logger

from com_gui.utils.modal_dialog import ModalDialogSettings
from com_gui.utils.settings_utils import ByteArraySetting

settings_file_name = os.path.normpath(
    os.path.join(os.path.expanduser('~'), 'Documents', 'ShnaiderPavel', 'CommunalPayments', 'settings.json'))


@dataclass()
class TableSettings:
    state: ByteArraySetting = ByteArraySetting()


@dataclass()
class MainWindowSettings:
    geometry: ByteArraySetting = ByteArraySetting()

    table: TableSettings = TableSettings()


@dataclass()
class GoogleSpreadSheetSettings:
    credential_file: str = ''
    spread_sheet_id: str = ''


@dataclass()
class Settings:
    main_window: MainWindowSettings = MainWindowSettings()
    google_spread_sheet: GoogleSpreadSheetSettings = GoogleSpreadSheetSettings()

    modal_dialogs_settings: ModalDialogSettings = ModalDialogSettings()

    def save(self):
        with self.prepare_to_save():
            dict_data = asdict(self)
            json_data = json.dumps(dict_data, indent=4)
            os.makedirs(os.path.dirname(settings_file_name), exist_ok=True)
            with open(settings_file_name, 'w+') as settings_file_:
                settings_file_.write(json_data)

    @contextmanager
    def prepare_to_save(self):
        save_callback = self.modal_dialogs_settings.save_callback
        try:
            self.modal_dialogs_settings.save_callback = None
            yield
        finally:
            self.modal_dialogs_settings.save_callback = save_callback

    @staticmethod
    def load():
        def default_settings():
            settings = Settings()
            settings.save()
            return settings

        if os.path.isfile(settings_file_name):
            try:
                with open(settings_file_name, 'r') as settings_file:
                    json_data = settings_file.read()
                    data = json.loads(json_data)
                    return from_dict(Settings, data)

            except Exception:
                logger.warning(f"Cant load config with error: {format_exc()}")
                return default_settings()
        else:
            return default_settings()


settings = Settings.load()
