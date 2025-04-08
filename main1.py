import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from flask import Flask

# 🔐 TOKEN va CHANNEL_ID to'g'ridan-to'g'ri
TOKEN = "7949948928:AAEneWduqNL-nWKBuLHhCgM_GNLrRDSGYQk"
HR_CHANNEL_ID = "@human_resource_hr"

# Bot va Flask sozlash
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return "Bot is running!"

PORT = int(os.environ.get("PORT", 5000))

# Holatlar guruhi
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

# Klaviaturalar
def gender_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Erkak"), KeyboardButton(text="Ayol")]],
                                resize_keyboard=True, one_time_keyboard=True)

def marital_status_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Uylangan"), KeyboardButton(text="Uylanmagan")],
        [KeyboardButton(text="Turmushga chiqqan"), KeyboardButton(text="Turmushga chiqmagan")]
    ], resize_keyboard=True, one_time_keyboard=True)

def phone_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]],
                                resize_keyboard=True, one_time_keyboard=True)

def student_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]],
                                resize_keyboard=True, one_time_keyboard=True)

def education_form_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Kunduzgi")],
        [KeyboardButton(text="Sirtqi")],
        [KeyboardButton(text="Kechki")]
    ], resize_keyboard=True, one_time_keyboard=True)

# Boshlanish komandasi
@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Rezyume to‘ldirish uchun kerakli ma'lumotlarni yuboring.")
    await asyncio.sleep(1)
    await message.answer("👤 To‘liq ismingizni kiriting:")
    await state.set_state(ResumeForm.full_name)

@dp.message(ResumeForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("📅 Tug‘ilgan kuningizni yozing (masalan: 01/01/1990):")
    await state.set_state(ResumeForm.age)

@dp.message(ResumeForm.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("🧍 Jinsingizni tanlang:", reply_markup=gender_keyboard())
    await state.set_state(ResumeForm.gender)

@dp.message(ResumeForm.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("📍 Yashash manzilingiz:")
    await state.set_state(ResumeForm.location)

@dp.message(ResumeForm.location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("🏢 Oxirgi ish joyingiz va nega bo‘shagansiz?")
    await state.set_state(ResumeForm.work_experience)

@dp.message(ResumeForm.work_experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(work_experience=message.text)
    await message.answer("💍 Oilaviy holatingiz:", reply_markup=marital_status_keyboard())
    await state.set_state(ResumeForm.marital_status)

@dp.message(ResumeForm.marital_status)
async def process_marital_status(message: types.Message, state: FSMContext):
    await state.update_data(marital_status=message.text)
    await message.answer("💰 Oylik maosh istagingiz (so‘mda):")
    await state.set_state(ResumeForm.salary_expectation)

@dp.message(ResumeForm.salary_expectation)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary_expectation=message.text)
    await message.answer("📞 Telefon raqam yuboring:", reply_markup=phone_keyboard())
    await state.set_state(ResumeForm.phone_number)

@dp.message(ResumeForm.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone_number=phone)
    await message.answer("🎓 Studentmisiz?", reply_markup=student_keyboard())
    await state.set_state(ResumeForm.student_status)

@dp.message(ResumeForm.student_status)
async def process_student_status(message: types.Message, state: FSMContext):
    await state.update_data(student_status=message.text)
    if message.text.lower() == "ha":
        await message.answer("Ta'lim shaklini tanlang:", reply_markup=education_form_keyboard())
        await state.set_state(ResumeForm.education_form)
    else:
        await message.answer("📸 Iltimos, fotosurat yuboring:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ResumeForm.photo)

@dp.message(ResumeForm.education_form)
async def process_education_form(message: types.Message, state: FSMContext):
    await state.update_data(education_form=message.text)
    await message.answer("📸 Iltimos, fotosurat yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ResumeForm.photo)

@dp.message(ResumeForm.photo)
async def process_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Faqat rasm yuboring.")
        return
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    data = await state.get_data()

    resume = (
        f"📄 <b>Yangi ariza</b>\n\n"
        f"👤 Ism: {data['full_name']}\n"
        f"🎂 Yosh: {data['age']}\n"
        f"⚥ Jinsi: {data['gender']}\n"
        f"📍 Yashash joyi: {data['location']}\n"
        f"🏢 Ish tajribasi: {data['work_experience']}\n"
        f"💍 Oilaviy holat: {data['marital_status']}\n"
        f"💰 Maosh istagi: {data['salary_expectation']} so‘m\n"
        f"📱 Telefon: {data['phone_number']}\n"
        f"🎓 Student: {data['student_status']}\n"
        f"📘 Ta'lim shakli: {data.get('education_form', 'Ko‘rsatilmagan')}\n"
        f"🆔 Telegram: @{message.from_user.username or 'yo‘q'}"
    )

    await bot.send_photo(chat_id=HR_CHANNEL_ID, photo=photo_id, caption=resume, parse_mode="HTML")
    await message.answer("✅ Arizangiz qabul qilindi. Rahmat!", reply_markup=ReplyKeyboardRemove())
    await state.clear()

# Asosiy funksiya
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=PORT)).start()
    asyncio.run(main())
