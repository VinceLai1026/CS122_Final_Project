import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

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
        print(f"Temperature range: {city_data['Temperature (°C)'].min():.1f}°C to {city_data['Temperature (°C)'].max():.1f}°C")
        print(f"Average temperature: {city_data['Temperature (°C)'].mean():.1f}°C")
        print(f"Average humidity: {city_data['Humidity (%)'].mean():.1f}%")

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
    
    # Find highest and lowest humidity
    highest_humidity = df.loc[df['Humidity (%)'].idxmax()]
    lowest_humidity = df.loc[df['Humidity (%)'].idxmin()]
    
    print(f"\nHighest humidity recorded: {highest_humidity['Humidity (%)']:.1f}%")
    print(f"City: {highest_humidity['City']}, {highest_humidity['State']}")
    print(f"Time: {highest_humidity['Timestamp']}")
    
    print(f"\nLowest humidity recorded: {lowest_humidity['Humidity (%)']:.1f}%")
    print(f"City: {lowest_humidity['City']}, {lowest_humidity['State']}")
    print(f"Time: {lowest_humidity['Timestamp']}")

def create_city_comparison_visualizations(df):
    """Create visualizations comparing the searched cities."""
    print("\n=== Creating City Comparison Visualizations ===")
    
    # Set style to a built-in matplotlib style
    plt.style.use('ggplot')
    
    # 1. Temperature Comparison Bar Chart
    plt.figure(figsize=(12, 6))
    city_avg_temp = df.groupby(['City', 'State'])['Temperature (°C)'].mean().sort_values(ascending=False)
    city_avg_temp.plot(kind='bar')
    plt.title('Average Temperature by City')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('city_temperature_comparison.png')
    plt.close()
    
    # 2. Temperature Range by City
    plt.figure(figsize=(12, 6))
    city_temp_ranges = df.groupby(['City', 'State']).agg({
        'Temperature (°C)': ['min', 'max']
    })
    city_temp_ranges.plot(kind='bar')
    plt.title('Temperature Range by City')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('city_temperature_ranges.png')
    plt.close()
    
    # 3. Latest Weather Conditions
    latest_data = df.sort_values('Timestamp').groupby(['City', 'State']).last()
    plt.figure(figsize=(12, 6))
    plt.bar(latest_data.reset_index()['City'], latest_data['Temperature (°C)'])
    plt.title('Latest Temperature by City')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('latest_temperatures.png')
    plt.close()

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
    create_city_comparison_visualizations(df)
    
    print("\nAnalysis complete! Check the generated PNG files for visualizations:")
    print("- city_temperature_comparison.png")
    print("- city_temperature_ranges.png")
    print("- latest_temperatures.png")

if __name__ == "__main__":
    main() 