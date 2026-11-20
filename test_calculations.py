
from utils.data_loader import get_player_data
from utils.calculations import build_comparison_table

# Load the cleaned dataset
df = get_player_data()

# Build the player comparison table
comparison = build_comparison_table(df)

# Display the results
print("\n--- PLAYER COMPARISON ---")
print(comparison.to_string(index=False))
