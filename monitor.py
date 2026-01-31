import asyncio
import google.generativeai as genai
import requests
import json
from telethon import TelegramClient, events

# --- НАСТРОЙКИ ---
API_ID = 38505616 
API_HASH = '1c0397c2337a6e1eb93818e884258edb'
GEMINI_KEY = "AIzaSyBwEX3JAQ1zi6-nvDuV-Z5A3sbtEy_ZYVM" 
FIREBASE_URL = "https://skywatcher-e6b95-default-rtdb.europe-west1.firebasedatabase.app/targets.json"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro') 

MONITOR_CHANNELS = [
    'vanek_nikolaev', 'monitor_news_ua', 'air_alert_ua', 'realkiev', 'kyiv_n', 
    'odessa_infonews', 'mykolaiv_live', 'kharkiv_life', 'dnepr_operativ', 
    'chernigov_chernigiv1', 'TM1602'
]

client = TelegramClient('skywatcher_session', API_ID, API_HASH)

async def get_coords_from_gemini(text):
    prompt = f"""
    Анализ текста: "{text}"
    Если есть угроза, верни ТОЛЬКО JSON:
    {{
      "lat": 46.48, 
      "lng": 30.72, 
      "type": "missile", 
      "city": "Одесса", 
      "region": "Odesa"
    }}
    Области для "region" (СТРОГО): Kyiv, Odesa, Mykolaiv, Kharkiv, Dnipropetrovsk, Kherson, Lviv, Zaporizhzhia, Chernihiv, Sumy, Poltava, Vinnytsia, Cherkasy.
    Если угрозы нет, верни {{"lat": null}}.
    """
    try:
        # Используем синхронный вызов внутри асинхронной обертки для стабильности
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        
        res_text = response.text.strip()
        if "```" in res_text:
            res_text = res_text.split("```")[1].replace("json", "").strip()
        
        return json.loads(res_text)
    except Exception as e:
        print(f"⚠️ Ошибка ИИ: {e}")
        return None

@client.on(events.NewMessage())
async def handler(event):
    if not event.message.text: return
    
    chat = await event.get_chat()
    username = getattr(chat, 'username', 'unknown')

    if username and username.lower() in [c.lower() for c in MONITOR_CHANNELS]:
        print(f"📩 Сообщение из @{username}: {event.message.text[:50]}...")
        
        # ВАЖНО: здесь мы ждем (await) результат работы ИИ
        data = await get_coords_from_gemini(event.message.text)
        
        if data and data.get("lat"):
            requests.post(FIREBASE_URL, json=data)
            print(f"🚀 ОТПРАВЛЕНО: {data['city']} ({data['region']})")

async def main():
    print("🛰 SkyWatcher ЗАПУСКАЕТСЯ...")
    await client.start()
    print("✅ РАДАР ОНЛАЙН!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹ Выключено.")