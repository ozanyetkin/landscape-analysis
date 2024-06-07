import pandas as pd

# Read the data from the CSV file
data = pd.read_csv("data/yenimahalle/park.csv")

# Fill the missing values in the renewed column with the mean of the column
data["renewed"] = data["renewed"].fillna(data["renewed"].mean())
data["constructed"] = data["constructed"].fillna(data["constructed"].mean())

# Convert the area, constructed, and renewed columns to integer
data["area"] = data["area"].str.replace(",", "").astype(int)
data["constructed"] = data["constructed"].astype(int)
data["renewed"] = data["renewed"].astype(int)

print(data)