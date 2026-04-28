import requests
import pandas as pd
from datetime import datetime
import os

# Konfigurácia
LAT, LON = "48.3774", "17.5833"
FILENAME = 'weather_daily.csv'

def get_temp_at_hour(hourly_data, hour):
    # API vracia dáta ako zoznam hodín 00-23
    try:
        return hourly_data['temperature_2m'][hour]
    except (IndexError, KeyError):
        return None

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m&start_date={today}&end_date={today}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Chyba pripojenia k API")
        return

    data = response.json()
    hourly = data.get('hourly', {})

    # Získanie hodnôt v požadovaných časoch
    t7 = get_temp_at_hour(hourly, 7)
    t14 = get_temp_at_hour(hourly, 14)
    t21 = get_temp_at_hour(hourly, 21)

    if None in [t7, t14, t21]:
        print("Chýbajú dáta pre niektorý z požadovaných časov (7, 14 alebo 21)")
        return

    # Vzorec: (T7 + T14 + 2 * T21) / 4
    avg_temp = (t7 + t14 + (2 * t21)) / 4

    # Uloženie do CSV
    new_entry = pd.DataFrame({'Datum': [today], 'T7': [t7], 'T14': [t14], 'T21': [t21], 'Priemer': [round(avg_temp, 2)]})
    
    if os.path.exists(FILENAME):
        df = pd.read_csv(FILENAME)
        # Ak už záznam pre dnešok existuje, prepíšeme ho
        df = df[df['Datum'] != today]
        df = pd.concat([df, new_entry]).sort_values('Datum')
    else:
        df = new_entry

    df.to_csv(FILENAME, index=False)
    print(f"Dáta pre {today} uložené: Priemer = {avg_temp}")

if __name__ == "__main__":
    main()
