from aiogram import Router, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio
import requests
from app.config import settings


API_TOKEN = settings.TELEGRAM_TOKEN
bot = Bot(token=API_TOKEN)
router = Router()

user_currencies = {}
chat_id = None

def get_latest_price(symbol):
    params = {"symbol": symbol, "convert": "USD"}
    headers = {"X-CMC_PRO_API_KEY": settings.API_KEY}
    response = requests.get(settings.COINMARKETCAP_API_URL, params=params, headers=headers)
    data = response.json()
    try:
        price = data["data"][symbol]["quote"]["USD"]["price"]
    except KeyError as e:
        print(f"Error: {e}")
        print(f"Response data: {data}")
        return None
    return price

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global chat_id
    chat_id = message.chat.id
    await message.answer(
        "Приветствую!"
        "\nЯ бот для отслеживания курса выбранной криптовалюты."
        "\nВозможность отслеживания нескольких криптовалют одновременно,"
        " хранение минимум двух значений для каждой валюты максимальный"
        " и минимальный порог"
        "\nФормат сообщения для отслеживания курса: "
        "\n/add BTC 60 50",
    )

@router.message(Command("add"))
async def add_currency_handler(message: Message) -> None:
    global chat_id
    try:
        symbol, max_threshold, min_threshold = message.text.split()[1:]
        max_threshold = float(max_threshold)
        min_threshold = float(min_threshold)
        if chat_id not in user_currencies:
            user_currencies[chat_id] = {}
        user_currencies[chat_id][symbol] = {"max_threshold": max_threshold, "min_threshold": min_threshold}
        await message.answer(f"Добавлена криптовалюта {symbol} с порогами {max_threshold} и {min_threshold}")
    except ValueError:
        await message.answer("Неправильный формат сообщения. Используйте формат: BTC 60 50")

async def check_currencies_periodically():
    while True:
        global chat_id
        global user_currencies
        if chat_id is None or not user_currencies:
            await asyncio.sleep(1)
            continue
        prices = {}
        for symbol in user_currencies[chat_id].keys():
            price = get_latest_price(symbol)
            if price is not None:
                prices[symbol] = price
        # проверяем пороги
        notifications = []
        for symbol, thresholds in user_currencies[chat_id].items():
            if prices[symbol] >= thresholds["max_threshold"]:
                notifications.append(f"{symbol} выше максимального порога: {thresholds['max_threshold']}")
            elif prices[symbol] <= thresholds["min_threshold"]:
                notifications.append(f"{symbol} ниже минимального порога: {thresholds['min_threshold']}")
        if notifications:
            await bot.send_message(chat_id, "\n".join(notifications))
        await asyncio.sleep(60)

async def main():
    dp = Dispatcher()
    dp.include_router(router)

    asyncio.create_task(check_currencies_periodically())
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')