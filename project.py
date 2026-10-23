from dotenv import load_dotenv
import os
import requests

load_dotenv()
os.system('cls' if os.name == 'nt' else 'clear')

weather_api = os.getenv("API_KEY")
url = "https://api.openweathermap.org/data/2.5/weather"
url_geocoding = "https://api.openweathermap.org/geo/1.0/direct"

oras = input("Introduceti orasul: ")

response_geocoding = requests.get(url_geocoding, params={
    'q': oras,
    'limit': 1,
    'appid': weather_api
}).json()

if not response_geocoding:
    print("Orasul nu a fost gasit.")
else:
    lat = response_geocoding[0]['lat']
    lon = response_geocoding[0]['lon']

    raspuns = requests.get(url, params={
        'lat': lat,
        'lon': lon,
        'appid': weather_api,
        'units': 'metric',
        'lang': 'ro'
    }).json()
    print(raspuns)

starea_vremii = raspuns['weather'][0]['description']
temperatura=raspuns['main']['temp']
viteza_vantului=raspuns['wind']['speed']
print (f"Starea vremii in {oras} este: {starea_vremii}. Temperatura este de {temperatura}°C, iar viteza vantului este de {viteza_vantului} m/s.")