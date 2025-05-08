import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def load_and_prepare_data():
    """Load the weather data and prepare it for analysis."""
    try:
        df = pd.read_csv('weather_data.csv')
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except FileNotFoundError:
        print("Error: weather_data.csv file not found!")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_searched_cities(df):
    """Analyze weather patterns for cities that users have searched for."""
    print("\n=== Analysis of Searched Cities ===")
    
    # Get unique cities that have been searched
    searched_cities = df[['City', 'State']].drop_duplicates()
    print(f"\nNumber of unique cities searched: {len(searched_cities)}")
    print("\nCities that have been searched:")
    for _, row in searched_cities.iterrows():
        print(f"- {row['City']}, {row['State']}")
    
    # Calculate statistics for each searched city
    print("\nDetailed Statistics for Each Searched City:")
    for _, row in searched_cities.iterrows():
        city_data = df[(df['City'] == row['City']) & (df['State'] == row['State'])]
        
        print(f"\n{row['City']}, {row['State']}:")
        print(f"Number of times searched: {len(city_data)}")
        print(f"Latest temperature: {city_data['Temperature (°C)'].iloc[-1]:.1f}°C")
        print(f"Latest humidity: {city_data['Humidity (%)'].iloc[-1]:.1f}%")

def find_extremes(df):
    """Find extreme weather conditions among searched cities."""
    print("\n=== Extreme Weather Conditions ===")
    
    # Find hottest and coldest temperatures
    hottest = df.loc[df['Temperature (°C)'].idxmax()]
    coldest = df.loc[df['Temperature (°C)'].idxmin()]
    
    print(f"\nHottest temperature recorded: {hottest['Temperature (°C)']:.1f}°C")
    print(f"City: {hottest['City']}, {hottest['State']}")
    print(f"Time: {hottest['Timestamp']}")
    
    print(f"\nColdest temperature recorded: {coldest['Temperature (°C)']:.1f}°C")
    print(f"City: {coldest['City']}, {coldest['State']}")
    print(f"Time: {coldest['Timestamp']}")

def create_weather_visualization(df):
    """Create visualization of latest temperatures and humidity with extreme cities highlighted."""
    print("\n=== Creating Weather Visualizations ===")
    
    # Set style to a built-in matplotlib style
    plt.style.use('ggplot')
    
    # Get hottest, coldest, most humid, and least humid cities
    hottest_city = df.loc[df['Temperature (°C)'].idxmax()]
    coldest_city = df.loc[df['Temperature (°C)'].idxmin()]
    most_humid_city = df.loc[df['Humidity (%)'].idxmax()]
    least_humid_city = df.loc[df['Humidity (%)'].idxmin()]
    
    # Get latest weather conditions
    latest_data = df.sort_values('Timestamp').groupby(['City', 'State']).last()
    
    # 1. Temperature Visualization
    plt.figure(figsize=(12, 6))
    temp_colors = []
    for city_state in latest_data.index:
        if city_state[0] == hottest_city['City'] and city_state[1] == hottest_city['State']:
            temp_colors.append('red')
        elif city_state[0] == coldest_city['City'] and city_state[1] == coldest_city['State']:
            temp_colors.append('blue')
        else:
            temp_colors.append('gray')
    
    plt.bar(range(len(latest_data)), latest_data['Temperature (°C)'], color=temp_colors)
    plt.title('Latest Temperature by City\n(Red: Hottest, Blue: Coldest)')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(range(len(latest_data)), [f"{city}, {state}" for city, state in latest_data.index], rotation=45)
    plt.tight_layout()
    plt.savefig('latest_temperatures.png')
    plt.close()
    
    # 2. Humidity Visualization
    plt.figure(figsize=(12, 6))
    humidity_colors = []
    for city_state in latest_data.index:
        if city_state[0] == most_humid_city['City'] and city_state[1] == most_humid_city['State']:
            humidity_colors.append('green')  # Most humid in green
        elif city_state[0] == least_humid_city['City'] and city_state[1] == least_humid_city['State']:
            humidity_colors.append('orange')  # Least humid in orange
        else:
            humidity_colors.append('gray')
    
    plt.bar(range(len(latest_data)), latest_data['Humidity (%)'], color=humidity_colors)
    plt.title('Latest Humidity by City\n(Green: Most Humid, Orange: Least Humid)')
    plt.xlabel('City')
    plt.ylabel('Humidity (%)')
    plt.xticks(range(len(latest_data)), [f"{city}, {state}" for city, state in latest_data.index], rotation=45)
    plt.tight_layout()
    plt.savefig('latest_humidity.png')
    plt.close()

def get_coordinates(city, state):
    """Get latitude and longitude for a city using geopy."""
    geolocator = Nominatim(user_agent="weather_analysis")
    try:
        location = geolocator.geocode(f"{city}, {state}, USA")
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        time.sleep(1)
        return get_coordinates(city, state)
    except Exception as e:
        print(f"Error getting coordinates for {city}, {state}: {e}")
        return None

def create_weather_heatmap(df):
    """Create an interactive heatmap of temperatures across searched cities."""
    print("\n=== Creating Weather Heatmap ===")
    
    # Get latest weather conditions for each city
    latest_data = df.sort_values('Timestamp').groupby(['City', 'State']).last().reset_index()
    
    # Create a base map centered on the US
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    
    # Add temperature heatmap
    heat_data = []
    for _, row in latest_data.iterrows():
        coords = get_coordinates(row['City'], row['State'])
        if coords:
            # Normalize temperature to a 0-1 scale for better visualization
            # Assuming temperature range from -20°C to 40°C
            normalized_temp = (row['Temperature (°C)'] + 20) / 60
            heat_data.append([coords[0], coords[1], normalized_temp])
            
            # Add markers with popups
            popup_text = f"""
            <b>{row['City']}, {row['State']}</b><br>
            Temperature: {row['Temperature (°C)']:.1f}°C<br>
            Humidity: {row['Humidity (%)']:.1f}%
            """
            folium.CircleMarker(
                location=coords,
                radius=8,
                popup=folium.Popup(popup_text, max_width=300),
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.7
            ).add_to(m)
    
    # Add the heatmap layer
    HeatMap(heat_data).add_to(m)
    
    # Add a layer control
    folium.LayerControl().add_to(m)
    
    # Save the map
    m.save('weather_heatmap.html')
    print("Heatmap saved as 'weather_heatmap.html'")

def main():
    """Main function to run all analyses."""
    print("Starting Weather Data Analysis for Searched Cities...")
    
    # Load data
    df = load_and_prepare_data()
    if df is None:
        return
    
    # Run analyses
    analyze_searched_cities(df)
    find_extremes(df)
    
    # Create visualizations
    create_weather_visualization(df)
    create_weather_heatmap(df)
    
    print("\nAnalysis complete! Check the generated files for visualizations:")
    print("- latest_temperatures.png")
    print("- latest_humidity.png")
    print("- weather_heatmap.html")

if __name__ == "__main__":
    main() 