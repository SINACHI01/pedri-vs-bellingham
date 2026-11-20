
from utils.data_loader import (
    get_player_data,
    inspect_player_data
)

# Load and clean the dataset
df = get_player_data()

# Inspect the cleaned dataset
inspect_player_data(df)

# Display the first five records
print(df.head())


print("\n--- PLAYER COUNTS ---")
print(df["player"].value_counts())

print("\n--- COMPETITIONS ---")
print(df["competition"].unique())

print("\n--- DATA TYPES ---")
print(df.dtypes)