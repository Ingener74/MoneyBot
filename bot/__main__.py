# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from pathlib import Path
from time import perf_counter
from traceback import format_exc

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from dotenv import load_dotenv
from loguru import logger

from bot.processor import process_check
from bot.settings import settings, ExtractMethod
from bot.utils import write_execution_time

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


@dp.message_handler(commands=["method"])
async def method(message: types.Message):
    await message.answer(f"Extract method is {settings.extract_method}")


@dp.message_handler(commands=["method_api"])
async def method_api(message: types.Message):
    settings.extract_method = ExtractMethod.Api
    settings.save()
    await message.answer(f"Set extract method to {settings.extract_method}")


@dp.message_handler(commands=["method_sel"])
async def method_sel(message: types.Message):
    settings.extract_method = ExtractMethod.Selenium
    settings.save()
    await message.answer(f"Set extract method to {settings.extract_method}")


logger.info("Money bot started")
executor.start_polling(dp)
