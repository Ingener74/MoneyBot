# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime
from time import perf_counter
from traceback import format_exc

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from dotenv import load_dotenv
from loguru import logger

from json_utils import reformat_json
from constants import CREDENTIAL_FILE, products_config
from get_check import get_check
from money.product import Products

logger.add("money_bot.log", rotation="10 MB")

load_dotenv()
bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hello")


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

        if destination.endswith(".json"):
            json_file_name = destination
        else:
            get_check(destination)
            json_file_name = "download/check.json"

        logger.info("Чек получен")
        await message.answer("Чек получен")

        products = Products.from_json(json_file_name)

        shutil.copy(json_file_name, destination + ".orig.json")
        reformat_json(json_file_name, destination + ".reformat.json")

        logger.info(f"Чек обработан\n{products.numbered_list_of_names}")
        await message.answer(f"Чек обработан\n{products.numbered_list_of_names}")

        products.save_to_google_sheet(CREDENTIAL_FILE, os.environ["MONEY_SPREEDSHEET"], products_config)

        logger.info("Чек сохранён")
        await message.answer("Чек сохранён")
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
