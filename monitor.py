import asyncio
import google.generativeai as genai
import requests
import json
from telethon import TelegramClient, events

# --- НАСТРОЙКИ ---
API_ID = 23971253  # Твой API ID
API_HASH = 'твой_апи_хэш'
GEMINI_KEY = "ТВОЙ_GEMINI_API_KEY" # ВСТАВЬ СЮДА КЛЮЧ
FIREBASE_URL = "https://skywatcher-e6b95-default-rtdb.europe-west1.firebasedatabase.app/targets.json"

# Настройка Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Каналы для мониторинга
CHANNELS = ['vanek_nikolaev', 'realkiev', 'kyiv_n', 'monitor_news_ua']

client = TelegramClient('skywatcher_session', API_ID, API_HASH)

async def get_coords_from_gemini(text):
    prompt = f"""
    Проанализируй текст сообщения о военной угрозе: "{text}"
    Найди населенный пункт или область. Верни ТОЛЬКО JSON формат:
    {{"lat": широта, "lng": долгота, "type": "shahed" или "missile" или "pvo"}}
    Если в тексте 'мопед' или 'шахед' - тип shahed. Если 'ракета' - missile.
    Если координат нет, верни null.
    """
    try:
        response = model.generate_content(prompt)
        data = json.loads(response.text.replace('```json', '').replace('```', ''))
        return data
    except:
        return None

@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    msg = event.message.message
    print(f"📩 Новое сообщение: {msg[:50]}...")
    
    # Спрашиваем у Gemini координаты
    target = await get_coords_from_gemini(msg)
    
    if target and target.get("lat"):
        # Отправляем в Firebase
        requests.post(FIREBASE_URL, json=target)
        print(f"✅ Цель добавлена на карту: {target}")

async def main():
    print("🛰 Радар запущен. Жду сообщений...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())