import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo

# --- НАСТРОЙКИ ---
TOKEN = "8305017709:AAH4MkhV4rDzN3jOI0qZTyFHGWed7jWzZOU"

# Ссылка БЕЗ пробелов в начале
MAP_URL = "https://trachmaxim2809-spec.github.io/skywatcher-monitor/"

# Если хочешь, чтобы бот не падал из-за стикера, пока оставь так:
STICKER_ID = None
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
        [types.InlineKeyboardButton(text="🛰 ЗАПУСТИТЬ МОНИТОР (V2.0)", web_app=WebAppInfo(url=MAP_URL))],
        [types.InlineKeyboardButton(text="⚙️ Настройки", callback_data="set"),
         types.InlineKeyboardButton(text="📊 Статистика", callback_data="stat")]
    ])

    await message.answer(text=text, parse_mode="HTML", reply_markup=markup)
# Этот обработчик будет ловить любой присланный стикер и писать его ID
@dp.message(lambda message: message.sticker)
async def get_sticker_id(message: types.Message):
    sticker_id = message.sticker.file_id
    print(f"\n🎯 ID ТВОЕГО СТИКЕРА: {sticker_id}\n")
    await message.answer(f"ID этого стикера:\n<code>{sticker_id}</code>", parse_mode="HTML")
async def main():
    print("--- Бот SkyWatcher запущен успешно! ---")
    print("Ожидание команд от пользователей...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")