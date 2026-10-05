from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import pandas as pd

TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Telefon yuborish uchun klaviatura
contact_kb = ReplyKeyboardMarkup(resize_keyboard=True)
contact_kb.add(KeyboardButton("Telefon raqam yuborish", request_contact=True))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Iltimos, telefon raqamingizni yuboring:", reply_markup=contact_kb)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number

    # Telefon raqamiga qarab ishlab chiqaruvchini aniqlash
    kodlar_df = pd.read_excel("kodlar.xlsx")  # telefon-ishlab chiqaruvchi
    user_row = kodlar_df[kodlar_df["Telefon"] == phone]

    if user_row.empty:
        await message.answer("Sizning raqamingiz uchun ishlab chiqaruvchi topilmadi.")
        return

    producer = user_row.iloc[0]["Ishlab Chikaruvchi"]

    # Asosiy ma'lumotdan filtrlash
    df = pd.read_excel("Фыв.xlsx", header=2)
    filtered = df[df["Ишлаб Чикарвучи"] == producer]

    if filtered.empty:
        await message.answer("Bu ishlab chiqaruvchi uchun ma'lumot topilmadi.")
    else:
        report_text = filtered[["Unnamed: 2", "Unnamed: 4", "Unnamed: 7", "Unnamed: 9"]].to_string(index=False, header=False)
        await message.answer(f"Sizga tegishli hisobot:\n\n{report_text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)