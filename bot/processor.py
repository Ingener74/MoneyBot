import os
import shutil
from pathlib import Path

from bot.settings import ExtractMethod, settings
from constants import CREDENTIAL_FILE, products_config
from money.selenium_check_extractor import get_check as get_check_selenium
from json_utils import reformat_json
from money.api_check_extractor import get_check as get_check_api, Status
from money.product import Products


def process_check(original_check_file: Path) -> str:
    if original_check_file.suffix == ".json":
        json_file_name = original_check_file
    else:
        json_file_name = original_check_file.parent / (original_check_file.stem + ".json")
        if settings.extract_method == ExtractMethod.Api:
            result = get_check_api(os.environ["PROVERKA_CHECKA_TOKEN"], original_check_file, json_file_name)
            if result.status != Status.Success:
                return f"{result.description}\n{result.text}"
        else:
            get_check_selenium(str(original_check_file))
            shutil.copy(Path("download/check.json"), json_file_name)

    products = Products.from_json(str(json_file_name))

    shutil.copy(json_file_name, original_check_file.parent / (original_check_file.stem + ".orig.json"))
    reformat_json(json_file_name, original_check_file.parent / (original_check_file.stem + ".reformat.json"))

    products.save_to_google_sheet(CREDENTIAL_FILE, os.environ["MONEY_SPREEDSHEET"], products_config)

    return products.numbered_list_of_names
