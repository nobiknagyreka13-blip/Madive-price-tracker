import os
import requests
from datetime import datetime

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = f"""
🏝️ Maldives Price Tracker teszt

A rendszer elindult:
{datetime.now().strftime("%Y-%m-%d %H:%M")}

Telegram kapcsolat OK ✅
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(
url,
data={
"chat_id": CHAT_ID,
"text": message
}
)

print("Telegram teszt elküldve")
