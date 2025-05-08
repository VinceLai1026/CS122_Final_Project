from flask import Flask, render_template, request, send_file
import requests
import csv
from datetime import datetime, timedelta
import os
from analyze_weather import create_weather_heatmap, load_and_prepare_data

app = Flask(__name__)

API_KEY = "25931e218dfddc5eebc3e949a3a0882e"
WEATHER_DATA_FILE = "weather_data.csv"

def celsius_to_fahrenheit(c_temp):
    """Convert Celsius to Fahrenheit."""
    return round((c_temp * 9/5) + 32, 2)

def update_or_append_weather_data(timestamp, city, state, temp_fahrenheit, humidity):
    file_exists = os.path.isfile(WEATHER_DATA_FILE)
    current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    twenty_four_hours_ago = current_time - timedelta(hours=24)
    
    if not file_exists:
        # Create new file with header
        with open(WEATHER_DATA_FILE, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "City", "State", "Temperature (°F)", "Humidity (%)"])
            writer.writerow([timestamp, city, state, temp_fahrenheit, humidity])
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
            rows[i] = [timestamp, city, state, temp_fahrenheit, humidity]
            found = True
            break

    if not found:
        # Append new entry
        rows.append([timestamp, city, state, temp_fahrenheit, humidity])

    # Write all data back to file
    with open(WEATHER_DATA_FILE, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
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
            humidity = data["main"]["humidity"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Convert temperature to Fahrenheit if it's in Celsius
            temp_fahrenheit = temp if units == "imperial" else celsius_to_fahrenheit(temp)
            
            # Update or append weather data (always in Fahrenheit)
            try:
                update_or_append_weather_data(timestamp, city, state, temp_fahrenheit, humidity)
            except Exception as e:
                print(f"Error updating CSV: {e}")

            # Display temperature in user's preferred unit
            display_temp = temp_fahrenheit if units == "imperial" else round((temp_fahrenheit - 32) * 5/9, 2)
            unit_symbol = "°F" if units == "imperial" else "°C"

            weather_data = {
                "city": f"{city}, {state}",
                "temp": display_temp,
                "humidity": humidity,
                "unit_symbol": unit_symbol
            }
        else:
            weather_data = {"error": "City not found or invalid input."}

    return render_template('index.html', weather=weather_data)

@app.route('/heatmap')
def show_heatmap():
    """Generate and serve the weather heatmap."""
    # Load data and create heatmap
    df = load_and_prepare_data()
    if df is not None:
        create_weather_heatmap(df)
        return send_file('weather_heatmap.html')
    return "No weather data available", 404

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Changed port to 5002 to avoid conflicts
