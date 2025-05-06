import tkinter as tk
from tkinter import ttk
from fetch_weather import fetch_weather

def get_weather():
    city = city_var.get()
    fetch_weather(city, api_key)
    status_label.config(text=f"Weather data for {city} fetched and saved.")

api_key = "25931e218dfddc5eebc3e949a3a0882e"

root = tk.Tk()
root.title("Weather Insight")

city_label = tk.Label(root, text="Select City:")
city_label.pack()

city_var = tk.StringVar()
city_dropdown = ttk.Combobox(root, textvariable=city_var, values=["San Francisco", "Los Angeles", "New York"])
city_dropdown.pack()

fetch_button = tk.Button(root, text="Fetch Weather Data", command=get_weather)
fetch_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
