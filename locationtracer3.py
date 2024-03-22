import geolocation
import requests
from bs4 import BeautifulSoup
import folium
from datetime import datetime, timezone
import weather

# Define variables
target_ip = "127.0.0.1"
target_port = 80

# Send a GET request to the target
response = requests.get(f"http://{target_ip}:{target_port}")

# Parse the response
soup = BeautifulSoup(response.text, "html.parser")

# Extract IP address from response
ip_address = soup.find("div", {"class": "server-info"}).find("a").text

# Compare target IP address to extracted IP address
if ip_address == target_ip:
    print("Location traced!")
else:
    print("Location not traced.")

# Convert IP address to geographic location
location = geolocation.get_location_from_ip(ip_address)
print(f"Location: {location}")

# Create a folium map
map = folium.Map(location=[location[1], location[0]], zoom_start=8)

# Add a marker to the map
folium.Marker(location=location, popup=f"IP Address: {ip_address}").add_to(map)

# Get timezone information
timezone_info = timezone(location[2]).tzname(None)
map.timezone_info = timezone_info

# Add a time zone marker
folium.TimezoneMarker(location=location, timezone=timezone_info).add_to(map)

# Get weather information
weather_data = weather.weather(location[0], location[1])
map.weather_info = weather_data

# Add weather marker
folium.WeatherMarker(weather_data, location=location).add_to(map)

# Display the map
map.save("map.html")