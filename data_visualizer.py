import pandas as pd
import requests
import urllib.parse
import matplotlib.pyplot as plt

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


# Add the latitude and longitude to the data if the .csv file is not available
if "latitude" not in data.columns:
    data["latitude"], data["longitude"] = zip(*data["name"].map(get_lat_lon))

    # Save the data to a new CSV file
    data.to_csv("data/yenimahalle/park_preprocessed.csv", index=False)

# Read the latitude and longitude from the data
latitude = data["latitude"]
longitude = data["longitude"]

# Plot the latitude and longitude on a scatter plot
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Parks in Yenimahalle")

# Use the area to determine the size of the points
size = data["area"] / 10
# plt.scatter(longitude, latitude, s=size, alpha=0.5)

# Add the name of the parks to the plot as labels
for i, name in enumerate(data["name"]):
    plt.text(longitude[i], latitude[i], name.lower(), fontsize=8)

# Remove the texts that are too close to each other
plt.tight_layout()

# Change the color of the points based on the presence of saplings, resting, sports, playground, grass
colors = (
    data["playground"]
    + 2 * data["sports"]
    + 3 * data["resting"]
    + 4 * data["grass"]
    + 5 * data["saplings"]
)
plt.scatter(longitude, latitude, s=size, c=colors, alpha=0.5)

# Add a colorbar to the plot
cbar = plt.colorbar()
cbar.set_label("Attributes")

# Save the plot to a file
plt.savefig("data/yenimahalle/parks.png")
