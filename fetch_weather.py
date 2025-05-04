import requests
import csv

def fetch_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    # Extract temperature and humidity
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    
    # Save to CSV
    filename = f"{city}_weather.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["City", "Temperature (°C)", "Humidity (%)"])
        writer.writerow([city, temp, humidity])
    
    print(f"Weather data for {city} saved to {filename}")

api_key = "25931e218dfddc5eebc3e949a3a0882e"

# Example call
fetch_weather("San Francisco", api_key)
