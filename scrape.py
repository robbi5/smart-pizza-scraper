from datetime import datetime, timedelta

import dataset
import os
from dotenv import load_dotenv
from requests_html import HTMLSession

load_dotenv()

MACHINE_ID = os.environ["MACHINE_ID"]

session = HTMLSession()

# initialize session cookie
session.get("https://application.smart-machine.fr/")
# be a guest
session.post(
    "https://application.smart-machine.fr/connexion", data={"invite": "invite"}
)

now = datetime.now()
dt = now + (datetime.min - now) % timedelta(minutes=15)  # round to next 15 min
jour = dt.date().isoformat()
date = dt.isoformat(sep=" ")

print(f"Looking for products available at date={date}")
r = session.post(
    "https://application.smart-machine.fr/machine/init",
    data={"idMachine": MACHINE_ID, "jour": jour, "date": date},
)

db = dataset.connect()
table = db["products"]

for pizza in r.html.find(".pizza-wrapper .pizza"):
    stock = int(pizza.attrs["data-stock"])
    name = pizza.find(".name", first=True).text
    print(f"Found name={name} stock={stock}")
    table.insert(
        dict(machine=MACHINE_ID, name=name, stock=stock, timestamp=dt, scraped_at=now)
    )
