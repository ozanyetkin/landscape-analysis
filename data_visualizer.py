import pandas as pd
import requests
import urllib.parse
import matplotlib.colors
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
saplings = data["saplings"]
resting = data["resting"]
sports = data["sports"]
playground = data["playground"]
grass = data["grass"]

# Create a color map for the points, and store it with the labels to create a color bar legend
labels = ["saplings", "resting", "sports", "playground", "grass"]
colors = ["forestgreen", "blue", "red", "orange", "limegreen"]

def mix_colors(color1, color2):
    # Get the RGB values of the predefined matplotlib colors
    r1, g1, b1 = matplotlib.colors.to_rgba(color1)[:3]
    r2, g2, b2 = matplotlib.colors.to_rgba(color2)[:3]
    # Mix the RGB values
    r = (r1 + r2) / 2
    g = (g1 + g2) / 2
    b = (b1 + b2) / 2
    return (r, g, b)

# Create a color map for the points based on the presence of the attributes,
# mix the colors if multiple attributes are present, store the labels and colors for the legend
color_map = []
for i in range(len(data)):
    color = "white"
    for j, attribute in enumerate([saplings, resting, sports, playground, grass]):
        if attribute[i] == 1:
            if color == "white":
                color = colors[j]
            else:
                # Mix the colors if multiple attributes are present
                color = mix_colors(color, colors[j])
    color_map.append(color)

# Create a color bar legend
color_map_legend = []
for i, label in enumerate(labels):
    color_map_legend.append(
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=label,
            markerfacecolor=colors[i],
            markersize=10,
        )
    )

# Plot the points with the color map
plt.scatter(longitude, latitude, s=size, alpha=0.5, c=color_map)

# Add the color bar legend to the plot
plt.legend(handles=color_map_legend, loc="upper right")

# Show the plot
plt.show()

# Save the plot to a file
plt.savefig("data/yenimahalle/parks.png")
