# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime
from pathlib import Path
from time import perf_counter
from traceback import format_exc

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from dotenv import load_dotenv
from loguru import logger

from json_utils import reformat_json
from constants import CREDENTIAL_FILE, products_config
from money.check_extractor import get_check, Status
from money.product import Products

logger.add("money_bot.log", rotation="10 MB")

load_dotenv()
bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hello")


def process_check(original_check_file: Path) -> str:
    if original_check_file.suffix == ".json":
        json_file_name = original_check_file
    else:
        json_file_name = original_check_file.parent / (original_check_file.stem + '.json')
        result = get_check(os.environ['PROVERKA_CHECKA_TOKEN'], original_check_file, json_file_name)
        if result.status != Status.Success:
            return f"{result.description}\n{result.text}"

    products = Products.from_json(str(json_file_name))

    shutil.copy(json_file_name, original_check_file.parent / (original_check_file.stem + ".orig.json"))
    reformat_json(json_file_name, original_check_file.parent / (original_check_file.stem + ".reformat.json"))

    products.save_to_google_sheet(CREDENTIAL_FILE, os.environ["MONEY_SPREEDSHEET"], products_config)

    return products.numbered_list_of_names


@dp.message_handler(commands=[""])
@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.DOCUMENT])
async def echo(message: types.Message):
    start = perf_counter()

    successful = False
    destination = ""
    try:
        if message.photo:
            logger.info("Сообщение содержит фото...")
            dest = await message.photo[-1].download(destination_dir=".")
            logger.info(f"... {dest}")
        elif message.document:
            logger.info("Сообщение содержит документ...")
            dest = await message.document.download(destination_dir=".")
            logger.info(f"... {dest}")
        else:
            raise RuntimeError("No photo or document")

        destination = str(dest.name)
        destination = destination.replace("\\", "/")

        process_result = process_check(Path(destination))

        logger.info(process_result)
        await message.answer(process_result)
        successful = True
    except Exception:
        await message.answer(f"Произошла ошибка: {format_exc()}")

    finally:
        end = perf_counter()

        logger.info(f"Время выполнения {end - start:.2f} секунд")

        write_execution_time("benchmarks.txt", successful, end - start, datetime.now(), destination)


def write_execution_time(file_name: str, successful: bool, delta: float, datetime: datetime, destination: str):
    with open(file_name, "a") as bench_file:
        bench_file.write(f"{destination};{successful};{datetime.strftime('%H:%M:%S-%d.%m.%Y')};{delta:.2f}\n")


if __name__ == "__main__":
    logger.info("Money bot started")
    executor.start_polling(dp)
