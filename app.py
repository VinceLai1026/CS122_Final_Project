from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

API_KEY = "25931e218dfddc5eebc3e949a3a0882e"

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
            humidity = data["main"]["humidity"]

            # Save to CSV
            filename = f"{city}_{state}_weather.csv"
            header = ["City", f"Temperature ({unit_symbol})", "Humidity (%)"]
            with open(filename, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerow([f"{city},{state}", temp, humidity])

            unit_symbol = "°F" if units == "imperial" else "°C"

            weather_data = {
                "city": f"{city}, {state}",
                "temp": temp,
                "humidity": humidity,
                "unit_symbol": unit_symbol
}

        else:
            weather_data = {"error": "City not found or invalid input."}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
