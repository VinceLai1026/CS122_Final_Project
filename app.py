from flask import Flask, render_template, request
import requests
import csv
from datetime import datetime, timedelta
import os

app = Flask(__name__)

API_KEY = "25931e218dfddc5eebc3e949a3a0882e"
WEATHER_DATA_FILE = "weather_data.csv"

def fahrenheit_to_celsius(f_temp):
    return round((f_temp - 32) * 5/9, 2)

def update_or_append_weather_data(timestamp, city, state, temp_celsius, humidity):
    file_exists = os.path.isfile(WEATHER_DATA_FILE)
    current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    twenty_four_hours_ago = current_time - timedelta(hours=24)
    
    if not file_exists:
        # Create new file with header
        with open(WEATHER_DATA_FILE, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "City", "State", "Temperature (°C)", "Humidity (%)"])
            writer.writerow([timestamp, city, state, temp_celsius, humidity])
        return

    # Read existing data
    rows = []
    with open(WEATHER_DATA_FILE, "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header
        rows = list(reader)

    # Check for existing entry in last 24 hours
    found = False
    for i, row in enumerate(rows):
        row_time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        if (row[1] == city and row[2] == state and 
            row_time > twenty_four_hours_ago):
            # Update existing entry
            rows[i] = [timestamp, city, state, temp_celsius, humidity]
            found = True
            break

    if not found:
        # Append new entry
        rows.append([timestamp, city, state, temp_celsius, humidity])

    # Write all data back to file
    with open(WEATHER_DATA_FILE, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)

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

            # Update or append weather data
            try:
                update_or_append_weather_data(timestamp, city, state, temp_celsius, humidity)
            except Exception as e:
                print(f"Error updating CSV: {e}")

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
