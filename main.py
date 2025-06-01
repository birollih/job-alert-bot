import requests
from bs4 import BeautifulSoup
import os
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = "https://isinolsun.com/is-ilanlari/istanbul-kucukcekmece?jobSort=2"

last_title = ""

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def check_new_job():
    global last_title
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    job = soup.find("a", class_="job-list-item")
    if job:
        title = job.get_text(strip=True)
        link = "https://isinolsun.com" + job["href"]

        if title != last_title:
            send_telegram_message(f"📢 Yeni İş İlanı: {title}\n🔗 {link}")
            last_title = title

while True:
    check_new_job()
    time.sleep(3600)  # 1 saatte bir kontrol eder
