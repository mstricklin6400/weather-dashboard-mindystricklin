import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os
import pygame

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

# --- Tkinter UI ---
root = tk.Tk()
root.title("Weather Persona")
root.geometry("400x500")
root.resizable(False, False)

# --- UI Elements ---
title_label = tk.Label(root, text="🌤️ Weather Persona App", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

city_entry = tk.Entry(root, width=30, font=("Helvetica", 12))
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city name")

fetch_button = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=lambda: fetch_weather())
fetch_button.pack(pady=10)

weather_result = tk.Label(root, text="", font=("Helvetica", 12))
weather_result.pack(pady=10)

avatar_label = tk.Label(root)
avatar_label.pack(pady=10)

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
        img = img.resize((200, 200))
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Image Error", f"Could not load avatar: {e}")
        return None

def load_music(weather_type):
    return os.path.join("music", f"{weather_type}.mp3")

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
            stop_music()
            return

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        weather_result.config(text=f"{city.title()}: {temp}°F, {description.capitalize()}")

        weather_type = get_weather_type(description)

        # Load and display avatar
        avatar_img = load_avatar(weather_type)
        if avatar_img:
            avatar_label.config(image=avatar_img)
            avatar_label.image = avatar_img  # Prevent garbage collection

        # Load and play music
        stop_music()
        music_path = load_music(weather_type)
        play_music(music_path)

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to fetch weather: {e}")

# --- Run App ---
root.mainloop()
