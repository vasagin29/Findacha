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
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

    except Exception as e:
        print("Ошибка загрузки SS.lv:", e)
        return


    soup = BeautifulSoup(response.text, "html.parser")
    
print("HTML размер:", len(response.text))

    links = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/msg/" in href:

            if href.startswith("/"):
                href = "https://www.ss.lv" + href

            if href not in links:
                links.append(href)


    new_links = [
        link for link in links
        if link not in seen
    ]

print("Найдено ссылок:", len(links))
print(links[:5])

if new_links:

    if new_links:

        text = "🏡 Новые дачи SS.lv:\n\n"

        for link in new_links[:5]:
            text += link + "\n\n"

            seen.add(link)


        await bot.send_message(
            chat_id=CHAT_ID,
            text=text
        )


        save_seen(seen)


asyncio.run(check_ss())
