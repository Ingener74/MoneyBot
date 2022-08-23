import json
import os
from dataclasses import dataclass, asdict
from enum import Enum, auto
from pathlib import Path
from traceback import format_exc

from dacite import from_dict, Config
from loguru import logger


class ExtractMethod(str, Enum):
    Api = 'api'
    Selenium = 'selenium'


settings_file_name = Path.home() / "Documents/ShnaiderPavel/MoneyBot/settings.json"
os.makedirs(settings_file_name.parent, exist_ok=True)


@dataclass()
class Settings:
    extract_method: ExtractMethod = ExtractMethod.Api

    def save(self):
        dict_data = asdict(self)
        json_data = json.dumps(dict_data, indent=4)
        with open(settings_file_name, "w+") as settings_file_:
            settings_file_.write(json_data)

    @staticmethod
    def load():
        def default_settings():
            settings = Settings()
            settings.save()
            return settings

        if os.path.isfile(settings_file_name):
            try:
                with open(settings_file_name, "r") as settings_file:
                    json_data = settings_file.read()
                    data = json.loads(json_data)
                    return from_dict(Settings, data, config=Config(cast=[ExtractMethod]))

            except Exception:
                logger.warning(f"Cant load config with error: {format_exc()}")
                return default_settings()
        else:
            return default_settings()


settings = Settings.load()
