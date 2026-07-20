import os
import json
import yaml
import requests
from datetime import datetime

from hotels.dhigali import Dhigali

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Konfiguráció betöltése
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
# Korábbi árak betöltése
with open("prices.json", "r") as f:
    prices = json.load(f)
    
# Bekötött hotelek
hotels = [
    Dhigali( )
]

# TESZT árak - később ezt cseréljük valódi lekérésre
current_prices = {}

for hotel in hotels:
    current_prices[hotel.name] = hotel.get_price( )
    
    alerts = []

for hotel, price in current_prices.items():
    #Ha még nincs ár, átugorjuk
    if price is None:
        alerts.append(
            f"{hotel}\n"
            f"Nincs még ár adat."
        )
        continue
        
    old_price = prices.get(hotel, {}).get("price")



    if old_price:
    
        decrease = (old_price - price) / old_price * 100
    
    
        if price < old_price:
            alerts.append(
                f"📉 {hotel_name}\n"
                f"Régi ár: {old_price:,} Ft\n"
                f"Új ár: {price:,} Ft\n"
                f"Csökkenés: {decrease:.1f}%"
            )
    
    
        if decrease >= config["alerts"]["drop_percent"]:
            alerts.append(
                f"🚨 {hotel_name}\n"
                f"Áresés nagyobb mint "
                f"{config['alerts']['drop_percent']}%"
             )
    
    
    if price < config["alerts"]["price_below_huf"]:
        alerts.append(
            f"💚 {hotel_name}\n"
            f"2,3 millió Ft alatti ár!\n"
            f"{price:,} Ft"
        )


    prices[hotel_name] = {
        "price": price,
        "checked": datetime.now().isoformat()
        }



# Árnapló mentése
with open("prices.json", "w") as f:
    json.dump(prices, f, indent=2)



# Telegram üzenet
if alerts:
    message = "\n\n".join(alerts)
else:
    message = "✅ Ellenőrzés kész. Nincs új riasztás."


requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)


print("Tracker finished")
