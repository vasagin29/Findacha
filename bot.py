import os
import json
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.ss.lv/ru/real-estate/homes-summer-residences/daugavpils-and-reg/daugavpils/"

FILE = "seen.json"


def load_seen():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=2)


async def check_ss():
    bot = Bot(token=TOKEN)

    seen = load_seen()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

    except Exception as e:
        print("Ошибка загрузки SS.lv:", repr(e), flush=True)
        return

    print("HTML размер:", len(response.text), flush=True)

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/msg/" in href:
            if href.startswith("/"):
                href = "https://www.ss.lv" + href

            if href not in links:
                links.append(href)

    print("Найдено ссылок:", len(links), flush=True)
    print(links[:5], flush=True)

    new_links = [
        link for link in links
        if link not in seen
    ]

    print("Новых ссылок:", len(new_links), flush=True)

    if not new_links:
        print("Новых объявлений нет.", flush=True)
        return

    text = "🏡 Новые дачи SS.lv:\n\n"

    for link in new_links[:5]:
        text += link + "\n\n"

    print("Пытаюсь отправить сообщение...", flush=True)

    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=text
        )
        print("✅ Сообщение успешно отправлено!", flush=True)

    except Exception as e:
        print("❌ Ошибка Telegram:", repr(e), flush=True)
        raise

    for link in new_links[:5]:
        seen.add(link)

    save_seen(seen)
    print("✅ seen.json обновлён", flush=True)


asyncio.run(check_ss())
