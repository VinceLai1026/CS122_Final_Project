from flask import Flask, render_template, request
import requests
import csv
from datetime import datetime
import os

app = Flask(__name__)

API_KEY = "25931e218dfddc5eebc3e949a3a0882e"
WEATHER_DATA_FILE = "weather_data.csv"

def fahrenheit_to_celsius(f_temp):
    return round((f_temp - 32) * 5/9, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    unit_symbol = ""  
    if request.method == 'POST':
        city = request.form['city']
        state = request.form['state']
        query = f"{city},{state},US"
        units = request.form['units']
        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units={units}"

        response = requests.get(url)
        data = response.json()

        if data.get("main"):
            temp = data["main"]["temp"]
            # Convert to Celsius if the temperature is in Fahrenheit
            temp_celsius = fahrenheit_to_celsius(temp) if units == "imperial" else temp
            humidity = data["main"]["humidity"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unit_symbol = "°F" if units == "imperial" else "°C"

            # Save to single CSV file (always in Celsius)
            file_exists = os.path.isfile(WEATHER_DATA_FILE)
            try:
                with open(WEATHER_DATA_FILE, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if not file_exists:
                        # Write header if file doesn't exist
                        writer.writerow(["Timestamp", "City", "State", "Temperature (°C)", "Humidity (%)"])
                    writer.writerow([timestamp, city, state, temp_celsius, humidity])
            except Exception as e:
                print(f"Error writing to CSV: {e}")

            weather_data = {
                "city": f"{city}, {state}",
                "temp": temp,  # Keep original temperature for display
                "humidity": humidity,
                "unit_symbol": unit_symbol
            }
        else:
            weather_data = {"error": "City not found or invalid input."}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
