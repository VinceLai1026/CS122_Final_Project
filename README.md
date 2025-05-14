# CS122 Final Project

## Project Title
**Weather Insight**

## Authors
- [VinceLai1026](https://github.com/VinceLai1026)
- [het8802](https://github.com/het8802)

## Project Description
This project creates a web-based Python application using Flask to allow users to explore real-time weather data. Users can input a city and state, fetch current weather conditions from the OpenWeatherMap API, view results directly in the browser, and save the data as a CSV file for analysis. The interface uses HTML and CSS for styling, and the backend fetches and organizes data automatically. This project makes weather analysis easy, accessible, and visually clear.

## Project Outline/Plan
- Set up GitHub and assign roles
- Build GUI (Flask with HTML/CSS)
- Fetch data from OpenWeatherMap API
- Store data as CSV file
- Analyze trends using NumPy, Folium and Matplotlib
- Visualize results
- Present final product

## Interface Plan
We built a web interface using Flask with two main user interactions:
1. A form where the user enters a city and state (abbreviation)
2. A result display showing the current temperature and humidity, plus an option to download the CSV

The design uses a modern HTML/CSS layout for clarity and ease of use.

## Data Collection and Storage Plan (written by Vince Lai)
We use the OpenWeatherMap API to fetch real-time weather data. The application retrieves the temperature (in °F) and humidity, then saves the data in a comprehensive CSV file. Each fetch call generates fresh data and overwrites the previous CSV for that city/state if the previous data was more than 24 hours old.

## Data Analysis and Visualization Plan (written by Het Tikawala)
We use NumPy, Folium and Matplotlib to process the stored CSV data. The analysis includes calculating averages and detecting anomalies. The results are visualized as plots showing weather trends in different cities and also create a heatmap to visualize the temperature in different cities.

## Technologies Used
- Python
- Flask
- HTML / CSS
- NumPy
- Matplotlib
- Requests (for API calls)
- CSV (for data storage)

## License
MIT License
