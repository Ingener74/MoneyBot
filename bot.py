# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import shutil
from datetime import datetime
from time import perf_counter
from traceback import format_exc

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from dotenv import load_dotenv
from loguru import logger

from Constants import purchase_config, CREDENTIAL_FILE
from Json import reformat_json
from Purchase.Purchase import Purchase
from app import process_expense
from get_check import get_check

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
            json_data = json.load(open(destination, "r"))
            json_data = json_data[0]["ticket"]["document"]["receipt"]
            json.dump(json_data, open("download/check.json", "w"))
        else:
            get_check(destination)

        logger.info("Чек получен")
        await message.answer("Чек получен")

        check = process_expense("download/check.json")

        shutil.copy("download/check.json", destination + ".orig.json")
        reformat_json("download/check.json", destination + ".reformat.json")

        logger.info(f"Чек обработан\n{check.purchase_list}")
        await message.answer(f"Чек обработан\n{check.purchase_list}")

        Purchase.save(
            check.date,
            check.purchases,
            purchase_config,
            CREDENTIAL_FILE,
            os.environ["MONEY_SPREEDSHEET"],
        )

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
