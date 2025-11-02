import requests
from bs4 import BeautifulSoup
import telebot
import time

# ====== إعدادات البوت ======
TOKEN = "8174031414:AAHgPEXLh39hr5G0ntXEkYp9fAQ4G3Yt0gI"   # عوّض بـ Token ديال البوت
CHANNEL = "@realestatepromotion"    # القناة ديالك

bot = telebot.TeleBot(TOKEN)

# ====== إعدادات البحث ======
BASE_URL = "https://www.mubawab.ma/fr/vente/appartements"  # مثال: بيع شقق
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ====== تابع جلب العقارات ======
def fetch_listings():
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"فشل الوصول للموقع: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    listings = []

    # استخراج العقارات
    for card in soup.find_all("div", class_="listingCard"):
        title_tag = card.find("h2", class_="card-title")
        link_tag = card.find("a", href=True)
        price_tag = card.find("span", class_="price")

        if title_tag and link_tag and price_tag:
            title = title_tag.text.strip()
            link = "https://www.mubawab.ma" + link_tag['href']
            price = price_tag.text.strip()
            listings.append(f"{title}\n{price}\n{link}")

    return listings

# ====== تابع إرسال العقارات للقناة ======
def send_to_telegram(listings):
    for listing in listings:
        try:
            bot.send_message(CHANNEL, listing)
            time.sleep(1)  # لتجنب الحظر
        except Exception as e:
            print("خطأ في الإرسال:", e)

# ====== السكريبت الرئيسي ======
if __name__ == "__main__":
    print("جاري جلب العقارات من Mubawab...")
    listings = fetch_listings()
    if listings:
        send_to_telegram(listings)
        print(f"تم إرسال {len(listings)} عقار للقناة ✅")
    else:
        print("لم يتم العثور على عقارات جديدة ❌")
