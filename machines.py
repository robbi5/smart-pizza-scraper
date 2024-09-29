import requests
import argparse

parser = argparse.ArgumentParser("machines")
parser.add_argument("lat", help="Latitude of the position you want to find machines")
parser.add_argument("lon", help="Longitude of the position you want to find machines")
args = parser.parse_args()


credentials = {
    'login': 'applimobile',
    'password': 'rZ0yK1mO2nJ4nK7r',
}

headers = {
    'user-agent': 'Dart/3.2 (dart:io)',
    'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    'host': 'atweb.smart-pizza.fr',
}

print(f"Looking for machines around lat={args.lat} lon={args.lon}")
data = {
    'latitude': args.lat,
    'longitude': args.lon,
    'with_baguettes': '0',
    'client_id': '0',
    'declinaison': '',
    **credentials
}
machines = requests.post(
    'https://atweb.smart-pizza.fr/webapi/geo_machines', 
    headers=headers, data=data).json()

for machine in machines:
    id = int(machine["idMachine"].strip())
    name = machine["nom"].strip()
    address = " ".join([str(machine.get("adresse_1", "")).strip(), str(machine.get("adresse_2", "")).strip()])
    geo = " ".join([str(machine.get("latitude", "")).strip(), str(machine.get("longitude", "")).strip()])

    print(f"#{id} - {name} - {address} ({geo})")

