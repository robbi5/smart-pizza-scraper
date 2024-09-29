from datetime import datetime, timedelta

import dataset
import os
from dotenv import load_dotenv

load_dotenv()

import requests

credentials = {
    'login': 'applimobile',
    'password': 'rZ0yK1mO2nJ4nK7r',
}

headers = {
    'user-agent': 'Dart/3.2 (dart:io)',
    'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    'host': 'atweb.smart-pizza.fr',
}

MACHINE_ID = os.environ["MACHINE_ID"]

now = datetime.now()
dt = now + (datetime.min - now) % timedelta(minutes=15)  # round to next 15 min
date = dt.isoformat(sep=" ")

print(f"Looking for products available at date={date}")
data = {
    'idMachine': MACHINE_ID,
    'date_heure': date,
    **credentials
}
stocks = requests.post(
    'https://atweb.smart-pizza.fr/webapi/stocks',
    headers=headers, data=data).json()

data = {
    'idMachine': MACHINE_ID,
    'lg': 'en',
    'afficherSansModeVente': '0',
    **credentials
}
pizzas = requests.post(
    'https://atweb.smart-pizza.fr/webapi/pizzas', 
    headers=headers, data=data).json()

db = dataset.connect()
table = db["products"]

for pizza in pizzas:
    id = pizza["idProduit"]
    stock = int(stocks["pizza"][id]["stock"])
    name = pizza["nom"].strip()
    print(f"Found name={name} stock={stock}")
    table.insert(
        dict(machine=MACHINE_ID, name=name, stock=stock, timestamp=dt, scraped_at=now)
    )
