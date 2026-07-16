import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.ss.lv/ru/real-estate/homes-summer-residences/daugavpils-and-reg/daugavpils/"

async def check_ss():
    bot = Bot(token=TOKEN)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(URL, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/msg/" in href:
            if href.startswith("/"):
                href = "https://www.ss.lv" + href

            if href not in links:
                links.append(href)

    if links:
        text = "🏡 Дачи SS.lv:\n\n"

        for link in links[:5]:
            text += link + "\n\n"

        await bot.send_message(
            chat_id=CHAT_ID,
            text=text
        )

asyncio.run(check_ss())
