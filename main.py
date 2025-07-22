import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os
import pygame
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# --- API Setup ---
API_KEY = "0a5a26c69d2686f3e8ce16ca52f16e0a"

# --- Initialize pygame for music ---
pygame.mixer.init()

# --- Music Playback ---
def play_music(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Music error:", e)

def stop_music():
    pygame.mixer.music.stop()

# --- GUI Setup ---
root = ttk.Window(themename="minty")
root.title("Weather App")
root.geometry("600x650")  # WIDER and taller window
root.resizable(False, False)

# --- UI Elements ---
title_label = ttk.Label(root, text="🌤️ Weather App", font=("Helvetica", 20, "bold"))
title_label.pack(pady=15)

city_entry = ttk.Entry(root, width=40, font=("Helvetica", 13))  # WIDER input
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name")

fetch_button = ttk.Button(root, text="Get Weather", bootstyle=PRIMARY, command=lambda: fetch_weather())
fetch_button.pack(pady=10)

weather_result = ttk.Label(root, text="", font=("Helvetica", 14))  # Larger font
weather_result.pack(pady=10)

prediction_label = ttk.Label(root, text="", font=("Helvetica", 13, "italic"), foreground="blue")
prediction_label.pack(pady=5)

avatar_label = ttk.Label(root)
avatar_label.pack(pady=20)

# --- Avatar Selection ---
def get_weather_type(description):
    description = description.lower()
    if "clear" in description:
        return "sunny"
    elif "cloud" in description:
        return "cloudy"
    elif "rain" in description or "drizzle" in description:
        return "rainy"
    elif "snow" in description:
        return "snowy"
    elif "mist" in description or "fog" in description:
        return "foggy"
    else:
        return "default"

def load_avatar(weather_type):
    path = os.path.join("avatars", f"{weather_type}.gif")
    try:
        img = Image.open(path)
        img = img.resize((250, 250))  # Slightly bigger avatar
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Image Error", f"Could not load avatar: {e}")
        return None

def load_music(weather_type):
    return os.path.join("music", f"{weather_type}.mp3")

# --- Forecast & Prediction ---
def fetch_forecast_and_predict(city):
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"

    try:
        response = requests.get(forecast_url)
        data = response.json()

        temps = []
        seen_days = set()

        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            if date not in seen_days:
                temps.append(entry["main"]["temp_max"])
                seen_days.add(date)
            if len(temps) == 5:
                break

        if len(temps) < 5:
            prediction_label.config(text="Not enough data to predict.")
            return

        x = np.arange(len(temps))
        coeffs = np.polyfit(x, temps, 1)
        model = np.poly1d(coeffs)
        tomorrow_temp = round(model(len(temps)), 2)

        prediction_label.config(text=f"📈 Predicted Temp Tomorrow: {tomorrow_temp}°F")

    except Exception as e:
        prediction_label.config(text="Prediction failed.")
        print("Forecast error:", e)

# --- Fetch Weather ---
def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Required", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            weather_result.config(text="City not found.")
            avatar_label.config(image="")
            prediction_label.config(text="")
            stop_music()
            return

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        weather_result.config(text=f"{city.title()}: {temp}°F, {description.capitalize()}")

        weather_type = get_weather_type(description)

        avatar_img = load_avatar(weather_type)
        if avatar_img:
            avatar_label.config(image=avatar_img)
            avatar_label.image = avatar_img

        stop_music()
        music_path = load_music(weather_type)
        play_music(music_path)

        fetch_forecast_and_predict(city)

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to fetch weather: {e}")

# --- Run App ---
root.mainloop()
