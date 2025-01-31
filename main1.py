import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "7596138177:AAEZ8UN_B0O7syKo7LPjC1m2o2JwxxmW45E"
HR_CHANNEL_ID = "@qwertybot01"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


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
    buttons = [
        [KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def education_form_keyboard():
    buttons = [
        [KeyboardButton(text="Kunduzgi")],
        [KeyboardButton(text="Sirtqi")],
        [KeyboardButton(text="Kechki")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def gender_keyboard():
    buttons = [
        [KeyboardButton(text="Erkak"), KeyboardButton(text="Ayol")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def marital_status_keyboard():
    buttons = [
        [KeyboardButton(text="Uylangan"), KeyboardButton(text="Uylanmagan")],
        [KeyboardButton(text="Turmushga chiqqan"), KeyboardButton(text="Turmushga chiqmagan")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)


def salary_keyboard():
    buttons = [
        [KeyboardButton(text="3 mln"), KeyboardButton(text="4 mln"), KeyboardButton(text="5 mln")]
    ]
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
    await message.answer("💵 Qancha oylik maosh olishni istaysiz? (so‘m)", reply_markup=salary_keyboard())
    await state.set_state(ResumeForm.salary_expectation)


@dp.message(ResumeForm.salary_expectation)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary_expectation=message.text)
    await message.answer("📱  telefon raqamingizni kiriting\n(masalan: +998XXXXXXXXX)", reply_markup=phone_keyboard())
    await state.set_state(ResumeForm.phone_number)


@dp.message(ResumeForm.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

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
        # Tugmani olib tashlash
        await message.answer("🎓 O‘z foto suratingizni yuboring.", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ResumeForm.photo)


@dp.message(ResumeForm.education_form)
async def process_education_form(message: types.Message, state: FSMContext):
    education_form = message.text
    await state.update_data(education_form=education_form)

    # Foto yuborishga chaqirish va tugmani olib tashlash
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

    student_status = user_data['student_status']
    education_form = user_data.get('education_form', None)

    # Agar student "Ha" deb javob bergan bo'lsa va ta'lim shakli tanlangan bo'lsa
    if student_status.lower() == "ha" and education_form:
        education_info = f"Ha, {education_form}"
    else:
        # Agar student "Yo‘q" deb javob bergan bo'lsa yoki ta'lim shakli tanlanmagan bo'lsa
        education_info = f"{student_status}"

    resume_text = (
        f"📄 **Yangi ariza kelib tushdi!**\n\n"
        f"👤 Ism: {user_data['full_name']}\n"
        f"🎂 Yosh: {user_data['age']}\n"
        f"⚥ Jinsi: {user_data['gender']}\n"
        f"🎓 Studentmisiz: {education_info}\n"
        f"📍 Yashash joyi: {user_data['location']}\n"
        f"🏢 Ish tajribasi: {user_data['work_experience']}\n"
        f"💍 Oilaviy holat: {user_data['marital_status']}\n"
        f"💰 Maosh talabi: {user_data['salary_expectation']} so‘m\n"
        f"📱 Telefon: +{user_data['phone_number']}\n"
        f"📞 Telegram: @{message.from_user.username or 'No username'}\n"
    )

    await bot.send_photo(HR_CHANNEL_ID, photo_id, caption=resume_text)
    await message.answer("✅ Arizangiz qabul qilindi. Tez orada siz bilan bog'lanamiz!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
