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

# Convert the attributes to different columns separated by "+"
data["attributes"] = (
    data["attributes"].str.split("+").apply(lambda x: x if type(x) == list else [])
)

# Create a new column for each attribute and fill it with 1 if the attribute is present, 0 otherwise
data["saplings"] = data["attributes"].apply(lambda x: 1 if "fa" in x else 0)
data["resting"] = data["attributes"].apply(lambda x: 1 if "da" in x else 0)
data["sports"] = data["attributes"].apply(lambda x: 1 if "sp" in x else 0)
data["playground"] = data["attributes"].apply(lambda x: 1 if "ç" in x else 0)
data["grass"] = data["attributes"].apply(lambda x: 1 if "ya" in x else 0)

# Drop the attributes column
data = data.drop("attributes", axis=1)

# Save the preprocessed data to a new CSV file
data.to_csv("data/yenimahalle/park_preprocessed.csv", index=False)
