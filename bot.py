from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import pandas as pd

TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Телефон юбориш учун клавиатура
contact_kb = ReplyKeyboardMarkup(resize_keyboard=True)
contact_kb.add(KeyboardButton("Телефон рақам юбориш", request_contact=True))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Илтимос, телефон рақамингизни юборинг:", reply_markup=contact_kb)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number

    # Телефон рақамга қараб ишлаб чиқарувчини аниқлаш
    kodlar_df = pd.read_excel("kodlar.xlsx")  # телефон-ишлаб чиқарувчи
    user_row = kodlar_df[kodlar_df["Telefon"] == phone]

    if user_row.empty:
        await message.answer("Сизнинг рақам учун ишлаб чиқарувчи топилмади.")
        return

    producer = user_row.iloc[0]["Ishlab Chikaruvchi"]

    # Асосий маълумотдан фильтрлаш
    df = pd.read_excel("Фыв.xlsx", header=2)
    filtered = df[df["Ишлаб Чикарвучи"] == producer]

    if filtered.empty:
        await message.answer("Бу ишлаб чиқарувчи учун маълумот топилмади.")
    else:
        report_text = filtered[["Unnamed: 2", "Unnamed: 4", "Unnamed: 7", "Unnamed: 9"]].to_string(index=False, header=False)
        await message.answer(f"Сизга тегишли ҳисобот:\n\n{report_text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)