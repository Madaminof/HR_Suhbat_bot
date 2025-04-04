import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from flask import Flask

TOKEN = "7755544055:AAE3olrSnAh8iTEoxPQqYE6mVHsssh7-HQI"
HR_CHANNEL_ID = "@human_resource_hr"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Flask server yaratamiz (Render Web Service uchun)
app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"


# Render-da avtomatik portni o'qish
PORT = int(os.environ.get("PORT", 5000))


class ResumeForm(StatesGroup):
    full_name = State()
    age = State()
    gender = State()
    location = State()
    work_experience = State()
    marital_status = State()
    salary_expectation = State()
    phone_number = State()
    student_status = State()
    education_form = State()
    photo = State()


def student_keyboard():
    buttons = [[KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def education_form_keyboard():
    buttons = [[KeyboardButton(text="Kunduzgi")], [KeyboardButton(text="Sirtqi")], [KeyboardButton(text="Kechki")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def gender_keyboard():
    buttons = [[KeyboardButton(text="Erkak"), KeyboardButton(text="Ayol")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def marital_status_keyboard():
    buttons = [[KeyboardButton(text="Uylangan"), KeyboardButton(text="Uylanmagan")],
               [KeyboardButton(text="Turmushga chiqqan"), KeyboardButton(text="Turmushga chiqmagan")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def phone_keyboard():
    buttons = [[KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Assalomu aleykum! O'z rezyumeyingizni to'ldirish uchun savollarga javob bering.")
    await asyncio.sleep(1)
    await message.answer("👤 Toʻliq ismingizni kiriting.\n(masalan: Ivan Ivanov Ivanovich)")
    await state.set_state(ResumeForm.full_name)


@dp.message(ResumeForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("📅 Iltimos, tug'ilgan kuningizni kiriting.\n(masalan, 18/03/1995):")
    await state.set_state(ResumeForm.age)


@dp.message(ResumeForm.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("🧍‍♂️/🧍‍♀️ Jinsni tanlang", reply_markup=gender_keyboard())
    await state.set_state(ResumeForm.gender)


@dp.message(ResumeForm.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("🏠 Turar joy manzili \n(tuman, ko'cha/blok, uy, kvartira):")
    await state.set_state(ResumeForm.location)


@dp.message(ResumeForm.location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("Oldingi ikkita ish joyingiz va nima sababdan bo'shagansiz?")
    await state.set_state(ResumeForm.work_experience)


@dp.message(ResumeForm.work_experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(work_experience=message.text)
    await message.answer("Oilaviy holatingiz qanday?", reply_markup=marital_status_keyboard())
    await state.set_state(ResumeForm.marital_status)


@dp.message(ResumeForm.marital_status)
async def process_marital_status(message: types.Message, state: FSMContext):
    await state.update_data(marital_status=message.text)
    await message.answer("💵 Qancha oylik maosh olishni istaysiz? (so‘mda yozing, masalan: 5000000)")
    await state.set_state(ResumeForm.salary_expectation)


@dp.message(ResumeForm.salary_expectation)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary_expectation=message.text)
    await message.answer("📱 Telefon raqamingizni kiriting\n(masalan: +998XXXXXXXXX)", reply_markup=phone_keyboard())
    await state.set_state(ResumeForm.phone_number)


@dp.message(ResumeForm.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone_number=phone_number)
    await message.answer("🎓 Siz studentmisiz?", reply_markup=student_keyboard())
    await state.set_state(ResumeForm.student_status)


@dp.message(ResumeForm.student_status)
async def process_student_status(message: types.Message, state: FSMContext):
    student_status = message.text
    await state.update_data(student_status=student_status)
    if student_status.lower() == "ha":
        await message.answer("Ta'lim shaklini tanlang:", reply_markup=education_form_keyboard())
        await state.set_state(ResumeForm.education_form)
    else:
        await message.answer("🎓 O‘z foto suratingizni yuboring.", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ResumeForm.photo)


@dp.message(ResumeForm.education_form)
async def process_education_form(message: types.Message, state: FSMContext):
    await state.update_data(education_form=message.text)
    await message.answer("🎓 O‘z foto suratingizni yuboring.", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ResumeForm.photo)


@dp.message(ResumeForm.photo)
async def process_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Iltimos, faqatgina rasm yuboring.")
        return

    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    user_data = await state.get_data()

    resume_text = (
        f"📄 **Yangi ariza kelib tushdi!**\n\n"
        f"👤 Ism: {user_data['full_name']}\n"
        f"🎂 Yosh: {user_data['age']}\n"
        f"⚥ Jinsi: {user_data['gender']}\n"
        f"📍 Yashash joyi: {user_data['location']}\n"
        f"📞 Telegram: @{message.from_user.username or 'No username'}\n"
    )

    await bot.send_photo(HR_CHANNEL_ID, photo_id, caption=resume_text)
    await message.answer("✅ Arizangiz qabul qilindi.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    from threading import Thread

    Thread(target=lambda: app.run(host="0.0.0.0", port=PORT)).start()
    asyncio.run(main())
