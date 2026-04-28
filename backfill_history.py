import requests
import pandas as pd
from datetime import datetime, timedelta

# Konfigurácia
LAT, LON = "48.3774", "17.5833"
FILENAME = 'weather_daily.csv'

def fetch_data(start_date, end_date):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={LAT}&longitude={LON}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
    response = requests.get(url)
    return response.json()

def process_history():
    # Rozdelenie na dva bloky, aby sme neprekročili limity API
    ranges = [
        ("2026-01-01", "2026-03-31"),
        ("2026-04-01", datetime.now().strftime('%Y-%m-%d'))
    ]
    
    all_data = []

    for start, end in ranges:
        data = fetch_data(start, end)
        hourly = data.get('hourly', {})
        times = hourly.get('time', [])
        temps = hourly.get('temperature_2m', [])
        
        # Iterácia po dňoch
        num_days = len(times) // 24
        for d in range(num_days):
            # Indexy pre hodiny v rámci dňa
            base_idx = d * 24
            t7 = temps[base_idx + 7]
            t14 = temps[base_idx + 14]
            t21 = temps[base_idx + 21]
            
            # Výpočet priemeru podľa vzorca
            avg = (t7 + t14 + (2 * t21)) / 4
            
            all_data.append({
                'Datum': times[base_idx].split('T')[0],
                'T7': t7,
                'T14': t14,
                'T21': t21,
                'Priemer': round(avg, 2)
            })

    # Uloženie do CSV
    df = pd.DataFrame(all_data)
    df.to_csv(FILENAME, index=False)
    print(f"História úspešne zapísaná do {FILENAME}. Počet dní: {len(df)}")

if __name__ == "__main__":
    process_history()
