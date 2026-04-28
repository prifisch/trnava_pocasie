import requests
import pandas as pd
from datetime import datetime, timedelta # Pridaný import pre dátumy
import os

# 1. Dynamický výpočet dátumu (včerajší deň)
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# 2. Vloženie dátumu do URL pomocou f-stringu
URL = f"https://archive-api.open-meteo.com/v1/era5?latitude=48.3774&longitude=17.5833&start_date={yesterday}&end_date={yesterday}&hourly=temperature_2m,precipitation"

def fetch_data():
    response = requests.get(URL).json()
    # Tu berieme dáta, ktoré prišli z API
    # POZOR: Toto vráti zoznam hodnôt pre celý deň, nie len jedno číslo!
    # Ak chceš uložiť všetky hodiny, treba to trochu upraviť:
    return response['hourly']

# Získanie dát
data = fetch_data()
times = data['time']
temps = data['temperature_2m']
precip = data['precipitation']

# Uloženie všetkých hodín do CSV
new_data = []
for i in range(len(times)):
    new_data.append({
        'Cas': times[i],
        'Teplota_C': temps[i],
        'Zrazky_mm': precip[i]
    })

# Čítanie a zápis
df_new = pd.DataFrame(new_data)
if os.path.exists('data.csv'):
    df_old = pd.read_csv('data.csv')
    df = pd.concat([df_old, df_new], ignore_index=True)
else:
    df = df_new

df.to_csv('data.csv', index=False)
