import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

# Welcome label
label = tk.Label(root, text="Welcome to my Weather App")
label.pack(pady=10)

# Entry box for city input
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=10)

# Simulated weather fetch function
def fake_fetch_weather():
    city = city_entry.get()
    if city.strip() == "":
        label.config(text="Please enter a city name.")
    else:
        label.config(text=f"{city}: 72°F, Sunny")

# Button to trigger fetch
button = tk.Button(root, text="Get Weather", command=fake_fetch_weather)
button.pack(pady=10)

# Run the app
root.mainloop()


