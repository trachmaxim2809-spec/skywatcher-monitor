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

# Настройка Gemini - используем проверенную gemini-pro
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro') 

MONITOR_CHANNELS = [
    'vanek_nikolaev', 'monitor_news_ua', 'air_alert_ua', 
    'realkiev', 'kyiv_n', 'kiev_operativ',
    'odessa_infonews', 'mykolaiv_live', 'kherson_typichnyi',
    'kharkiv_life', 'dnepr_operativ', 'zaporozhye_vibor', 'donetsk_live',
    'vinnytsia_live', 'poltava_operativ', 'cherkasy_live', 'krop_live', 'zhytomyr_today',
    'chernigov_chernigiv1', 'sumy_today',
    'lviv_life', 'varta1_official', 'lutsk_live', 'frankivsk_city', 'ternopil_live', 'rivne_live7',
    'TM1602' 
]

client = TelegramClient('skywatcher_session', API_ID, API_HASH)

async def get_coords_from_gemini(text):
    prompt = f"""
    Текст: "{text}"
    Если в тексте есть угроза (шахед, ракета), выдели город и область.
    Верни ТОЛЬКО JSON:
    {{
      "lat": широта, 
      "lng": долгота, 
      "type": "missile", 
      "city": "Название города", 
      "region": "Название области на англ"
    }}
    Области пиши строго так: Kyiv, Odesa, Mykolaiv, Kharkiv, Dnipropetrovsk, Kherson, Lviv, Zaporizhzhia, Chernihiv, Sumy.
    Если это просто текст без угрозы, верни {{"lat": null}}.
    """
    # ... (остальной код функции без изменений)
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        res_text = response.text.strip()
        if "```" in res_text:
            res_text = res_text.split("```")[1].replace("json", "").strip()
        return json.loads(res_text)
    except Exception as e:
        print(f"⚠️ Ошибка Gemini: {e}")
        return None

@client.on(events.NewMessage())
async def handler(event):
    if not event.message.text: return
    
    chat = await event.get_chat()
    username = getattr(chat, 'username', None)

    if username and username.lower() in [c.lower() for c in MONITOR_CHANNELS]:
        print(f"📩 [ @{username} ]: {event.message.text[:50]}...")
        
        # Запускаем обработку в отдельном потоке, чтобы не тормозить Telegram
        data = await asyncio.to_thread(get_coords_from_gemini, event.message.text)
        
        if data and data.get("lat"):
            requests.post(FIREBASE_URL, json=data)
            print(f"🚀 ЦЕЛЬ В БАЗЕ: {data.get('city')} [{data.get('type')}]")

async def main():
    print("🛰 SkyWatcher ЗАПУСКАЕТСЯ...")
    await client.start()
    print("✅ РАДАР ОНЛАЙН! Жду сообщений...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹ Выключено.")