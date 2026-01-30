import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo

# --- НАСТРОЙКИ ---
TOKEN = "8305017709:AAH4MkhV4rDzN3jOI0qZTyFHGWed7jWzZOU" # Возьми свежий в @BotFather
# ID стикеров (узнай их через @idstickersbot после создания пака)
STICKER_SHAHED = "t.me/addstickers/tyrwwww" 

# Адрес твоей будущей карты (пока заглушка)
MAP_URL = "https://google.com" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # 1. Отправляем приветственный стикер
    try:
        await message.answer_sticker(sticker=STICKER_SHAHED)
    except Exception as e:
        print(f"Ошибка стикера: {e}. Проверь ID.")

    # 2. Формируем стильный текст
    text = (
        "🛰 <b>SkyWatcher: Tactical Monitor</b>\n"
        "━━━━━━━━━━━━━━\n"
        "⚪️ — <b>БПЛА «Shahed»</b>\n"
        "🔴 — <b>Крылатая ракета</b>\n"
        "🔵 — <b>Работа ПВО / Перехват</b>\n"
        "━━━━━━━━━━━━━━\n"
        "<i>Нажми кнопку ниже, чтобы развернуть тактическую карту в реальном времени.</i>"
    )

    # 3. Создаем кнопку для WebApp (Карты)
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗺 ОТКРЫТЬ ТАКТИЧЕСКУЮ КАРТУ", web_app=WebAppInfo(url=MAP_URL))],
        [types.InlineKeyboardButton(text="⚙️ Настройки", callback_data="set"),
         types.InlineKeyboardButton(text="📊 Статистика", callback_data="stat")]
    ])

    await message.answer(text=text, parse_mode="HTML", reply_markup=markup)

async def main():
    print("--- Бот SkyWatcher запущен успешно! ---")
    print("Ожидание команд от пользователей...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")