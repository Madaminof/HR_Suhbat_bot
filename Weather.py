import requests
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
import asyncio

# OpenWeatherMap API kaliti
API_KEY = "7b8da07fb6e1764fbba745c856834274"

# Telegram bot tokeni
TELEGRAM_TOKEN = "7596138177:AAEZ8UN_B0O7syKo7LPjC1m2o2JwxxmW45E"

viloyatlar = {
    "Toshkent": "Toshkent",
    "Samarqand": "Samarqand",
    "Buxoro": "Buxoro",
    "Farg'ona": "Farg'ona",
    "Andijon": "Andijon",
    "Namangan": "Namangan",
    "Navoiy": "Navoiy",
    "Jizzax": "Jizzax",
    "Qarshi": "Qarshi",
    "Termiz": "Termiz",
    "Olmaliq": "Olmaliq",
}


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},UZ&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_description = data["weather"][0]["description"]
        pressure = data["main"]["pressure"]
        visibility = data.get("visibility", "N/A")

        return (
            f"{hbold(city)}da ob-havo:\n"
            f"Harorat: {temp}°C\n"
            f"Namlik: {humidity}%\n"
            f"Shamol tezligi: {wind_speed} m/s\n"
            f"Ob-havo: {weather_description.capitalize()}\n"
            f"Bosim: {pressure} hPa\n"
            f"Ko'rinish masofasi: {visibility} m"
        )
    else:
        return f"{city} uchun ob-havo ma'lumotlari topilmadi."


# Bot va Dispatcher yaratish
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Salom! Men sizga O'zbekiston viloyatlarining ob-havo ma'lumotlarini taqdim eta olaman.\n"
        "Viloyat nomini kiriting.\nMasalan: /weather Toshkent"
    )


@dp.message(Command("weather"))
async def get_city_weather(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos, viloyat nomini kiriting. Masalan: /weather Toshkent")
        return
    city = args[1].strip()

    if city in viloyatlar:
        weather_info = get_weather(viloyatlar[city])
        await message.answer(weather_info)
    else:
        await message.answer(
            f"{city} nomli viloyat mavjud emas. Iltimos, to'g'ri nom kiriting.\nMasalan: /weather Toshkent"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())