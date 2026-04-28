import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Načítanie API kľúča z .env
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Trnava"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},SK&appid={API_KEY}&units=metric&lang=sk"
    response = requests.get(url)
    return response.json()

st.title(f"Aktuálne počasie v {CITY}")

if st.button("Obnoviť údaje"):
    data = get_weather()
    
    if data.get("cod") == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        
        st.metric(label="Teplota", value=f"{temp}°C")
        st.write(f"**Stav:** {desc.capitalize()}")
        st.write(f"**Vlhkosť:** {humidity}%")
    else:
        st.error("Nepodarilo sa načítať údaje. Skontroluj API kľúč.")
