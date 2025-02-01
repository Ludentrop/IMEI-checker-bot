import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import requests
import json

from config import settings


logging.basicConfig(level=logging.INFO)

TOKEN = settings.TOKEN.get_secret_value()
API_KEY = settings.API_KEY.get_secret_value()

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


async def check_imei(imei: str) -> dict:
    url = "https://api.imeicheck.net/v1/checks"
    headers = {"Authorization": f"Bearer {settings.API_KEY}"}
    body =  json.dumps({
        "deviceId": imei,
        "serviceId": 1})
    response = requests.post(url, headers=headers, data=body)
    return response.json()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in settings.WHITELIST_USERS:
        await message.reply("У вас нет доступа к этому боту.")
        return
    await message.answer("Чтобы проверить IMEI введите IMEI после команды /check")


@dp.message(Command("check"))
async def cmd_check_imei(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    if user_id not in settings.WHITELIST_USERS:
        await message.reply("У вас нет доступа к этому боту.")
        return

    if command.args is None:  # 20h This is delayed
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return

    try:
        imei = command.args
        if len(imei) != 15 or not imei.isdigit():
            raise ValueError("Неверный формат IMEI")

        result = await check_imei(imei)
        if result.get("status") == "success":
            info = result["data"]
            response_text = (
                f"IMEI: {info['imei']}\n"
                f"Brand: {info['brand']}\n"
                f"Model: {info['model']}\n"
                f"Status: {info['status']}"
            )
        else:
            response_text = "Ошибка при проверке IMEI."
        await message.reply(response_text)

    except IndexError:
        await message.reply("Используйте команду: /check <IMEI>")


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
