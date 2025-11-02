import requests
from bs4 import BeautifulSoup
import telebot

# ====== إعدادات البوت ======
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

bot = telebot.TeleBot(TOKEN)

# مثال طلب موقع
url = "https://www.mubawab.ma/fr/"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    # ... تحليل البيانات هنا ...
    bot.send_message(CHAT_ID, "مثال: الموقع خدم بنجاح ✅")
else:
    bot.send_message(CHAT_ID, f"فشل الوصول للموقع ❌ Status: {response.status_code}")
