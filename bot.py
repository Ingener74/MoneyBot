# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from traceback import format_exc

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from loguru import logger

from Constants import purchase_config, CREDENTIAL_FILE
from Purchase.Purchase import Purchase
from app import process_expense
from get_check import get_check

load_dotenv()
bot = Bot(token=os.environ['TOKEN'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello")


@dp.message_handler(commands=[''])
@dp.message_handler(content_types=['photo'])
async def echo(message: types.Message):
    destination = await message.photo[-1].download(destination_dir='.')

    try:
        destination = destination.name.replace('\\', '/')

        get_check(destination)

        await message.answer('Чек получен')

        check = process_expense('download/check.json')

        await message.answer(f"Чек обработан\n{check.purchase_list}")

        Purchase.save(check.date, check.purchases, purchase_config, CREDENTIAL_FILE, os.environ['MONEY_SPREEDSHEET'])

        await message.answer('Чек сохранён')
    except Exception:
        await message.answer(f"Произошла ошибка: {format_exc()}")


if __name__ == '__main__':
    logger.info('Money bot started')
    executor.start_polling(dp)
