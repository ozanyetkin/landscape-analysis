import pandas as pd
import requests
import urllib.parse

# Read the data from the CSV file
data = pd.read_csv("data/yenimahalle/park_preprocessed.csv")


# Get the name feature and call OpenStreetMap API to get the latitude and longitude
def get_lat_lon(name):
    # Encode the name to be used in the URL
    name_encoded = urllib.parse.quote(name)
    # Call the OpenStreetMap API
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={name_encoded}&format=json"
    )
    # Get the latitude and longitude from the response
    try:
        latitude = response.json()[0]["lat"]
        longitude = response.json()[0]["lon"]
    except IndexError:
        latitude = None
        longitude = None
    return latitude, longitude


# Add the latitude and longitude to the data
data["latitude"], data["longitude"] = zip(*data["name"].map(get_lat_lon))

print(data)
