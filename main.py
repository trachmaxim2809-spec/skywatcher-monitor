import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo

# --- НАСТРОЙКИ ---
TOKEN = "8305017709:AAH4MkhV4rDzN3jOI0qZTyFHGWed7jWzZOU"
MAP_URL = "https://trachmaxim2809-spec.github.io/skywatcher-monitor/"

# Здесь мы используем одно и то же имя переменной
STICKER_ID = None 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # 1. Отправляем приветственный стикер (только если ID указан)
    if STICKER_ID:
        try:
            await message.answer_sticker(sticker=STICKER_ID)
        except Exception as e:
            print(f"Ошибка стикера: {e}")

    # 2. Формируем стильный текст
    text = (
        "🛰 <b>SkyWatcher: Tactical Monitor</b>\n"
        "━━━━━━━━━━━━━━\n"
        "⚪️ — <b>БПЛА «Shahed»</b>\n"
        "🔴 — <b>Крылатая ракета</b>\n"
        "🔵 — <b>Работа ПВО / Перехват</b>\n"
        "━━━━━━━━━━━━━━\n"
        "<i>Нажми кнопку ниже, чтобы развернуть тактическую карту.</i>"
    )

    # 3. Создаем кнопки
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗺 ОТКРЫТЬ КАРТУ (NEW)", web_app=WebAppInfo(url=MAP_URL))],
        [types.InlineKeyboardButton(text="📊 Статистика", callback_data="stat")]
    ])

    await message.answer(text=text, parse_mode="HTML", reply_markup=markup)

# Обработчик для получения ID стикера
@dp.message(lambda message: message.sticker)
async def get_sticker_id(message: types.Message):
    sid = message.sticker.file_id
    print(f"\n🎯 ID ТВОЕГО СТИКЕРА: {sid}\n")
    await message.answer(f"ID этого стикера:\n<code>{sid}</code>", parse_mode="HTML")

async def main():
    print("--- Бот SkyWatcher запущен успешно! ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")
