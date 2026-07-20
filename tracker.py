import os
import json
import yaml
import requests
from datetime import datetime

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

with open("prices.json", "r") as f:
    prices = json.load(f)

# TESZT árak - később ezt cseréljük valódi lekérésre
current_prices = {
"Dhigali Maldives": 2450000,
"Cora Cora Maldives": 2700000,
"Hideaway Beach Resort & Spa": 3100000,
"Lily Beach Resort & Spa": 2900000
}

alerts = []

for hotel, price in current_prices.items():

    old_price = prices.get(hotel, {}).get("price")

    if old_price:
      decrease = (old_price - price) / old_price * 100

      if price < old_price:
        alerts.append(
            f"📉 {hotel}\n"
            f"Régi ár: {old_price:,} Ft\n"
            f"Új ár: {price:,} Ft\n"
            f"Csökkenés: {decrease:.1f}%"
        )

      if decrease >= config["alerts"]["drop_percent"]:
        alerts.append(
            f"🚨 {hotel}\n"
            f"Áresés >8%!"
         )

    if price < config["alerts"]["price_below_huf"]:
        alerts.append(
            f"🏝️ {hotel}\n"
            f"2,3 millió Ft alatti ár: {price:,} Ft"
        )

    prices[hotel] = {
        "price": price,
        "checked": datetime.now().isoformat()
    }


with open("prices.json", "w") as f:
    json.dump(prices, f, indent=2)


if alerts:
    message = "\n\n".join(alerts)
else:
    message = "✅ Ellenőrzés kész. Nincs új árriasztás."


requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Tracker finished")
