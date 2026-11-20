
import pandas as pd

from utils.data_loader import get_player_data

from utils.calculations import (
    calculate_career_totals,
    calculate_per_90,
    calculate_passing_accuracy,
    calculate_shot_conversion_rate,
    calculate_shots_on_target_percentage,
    build_comparison_table,
    calculate_seasonal_stats
)


# --------------------------------
# 1. LOAD DATA
# --------------------------------

df = get_player_data()

print("\nDATA LOADED SUCCESSFULLY")
print(f"Total records: {len(df)}")


# --------------------------------
# 2. CAREER TOTALS
# --------------------------------

career = calculate_career_totals(df)

print("\nCAREER TOTALS")
print(career.to_string(index=False))


# --------------------------------
# 3. CALCULATED METRICS
# --------------------------------

stats = calculate_per_90(career)
stats = calculate_passing_accuracy(stats)
stats = calculate_shot_conversion_rate(stats)
stats = calculate_shots_on_target_percentage(stats)

print("\nCALCULATED METRICS")

metrics = [
    "player",
    "goals_per_90",
    "assists_per_90",
    "tackles_per_90",
    "interceptions_per_90",
    "pass_accuracy",
    "shot_conversion_rate",
    "shots_on_target_percentage"
]

print(stats[metrics].round(2).to_string(index=False))


# --------------------------------
# 4. COMPARISON TABLE
# --------------------------------

comparison = build_comparison_table(df)

print("\nCOMPARISON TABLE")
print(comparison.to_string(index=False))


# --------------------------------
# 5. SEASONAL STATISTICS
# --------------------------------

seasonal = calculate_seasonal_stats(df)

print("\nSEASONAL STATISTICS")
print(seasonal.round(2).to_string(index=False))


# --------------------------------
# 6. BASIC VALIDATION CHECKS
# --------------------------------

print("\nVALIDATION CHECKS")

# Check for negative per-90 values
per_90_columns = [
    "goals_per_90",
    "assists_per_90",
    "tackles_per_90",
    "interceptions_per_90"
]

for column in per_90_columns:
    assert (stats[column].dropna() >= 0).all(), (
        f"Negative values found in {column}"
    )

print("PASS: Per-90 metrics contain no negative values.")


# Check passing accuracy
valid_passing = stats["pass_accuracy"].dropna()

assert valid_passing.between(0, 100).all(), (
    "Passing accuracy outside 0-100%"
)

print("PASS: Passing accuracy is within 0-100%.")


# Check shooting percentages
for column in [
    "shot_conversion_rate",
    "shots_on_target_percentage"
]:

    valid_values = stats[column].dropna()

    assert valid_values.between(0, 100).all(), (
        f"{column} outside 0-100%"
    )

print("PASS: Shooting percentages are within 0-100%.")


# Check shots on target do not exceed total shots
valid_shots = comparison.dropna(
    subset=["shots_on_target", "shots_attempted"]
)

assert (
    valid_shots["shots_on_target"]
    <= valid_shots["shots_attempted"]
).all(), "Shots on target exceed total shots."

print("PASS: Shots on target do not exceed total shots.")


print("\nALL VALIDATION CHECKS PASSED!")


# --------------------------------
# 7. DATA COVERAGE AUDIT
# --------------------------------

print("\nDATA COVERAGE AUDIT")

for player in sorted(df["player"].unique()):

    player_df = df[df["player"] == player]

    total_records = len(player_df)

    shooting_records = player_df.dropna(
        subset=[
            "goals",
            "shots_on_target",
            "shots_attempted"
        ]
    )

    passing_records = player_df.dropna(
        subset=[
            "passes_completed",
            "passes_attempted"
        ]
    )

    defensive_records = player_df.dropna(
        subset=[
            "tackles",
            "interceptions"
        ]
    )

    total_goals = player_df["goals"].sum(min_count=1)

    shooting_goals = shooting_records["goals"].sum(
        min_count=1
    )

    goal_coverage = (
        shooting_goals / total_goals * 100
        if pd.notna(total_goals) and total_goals > 0
        else float("nan")
    )

    print(f"\n{player}")
    print(f"Total records: {total_records}")

    print(
        f"Shooting records: "
        f"{len(shooting_records)}/{total_records}"
    )

    print(
        f"Goals represented in shooting records: "
        f"{shooting_goals}/{total_goals}"
    )

    print(
        f"Goal coverage: {goal_coverage:.2f}%"
        if pd.notna(goal_coverage)
        else "Goal coverage: N/A"
    )

    print(
        f"Passing records: "
        f"{len(passing_records)}/{total_records}"
    )

    print(
        f"Complete defensive records: "
        f"{len(defensive_records)}/{total_records}"
    )


# --------------------------------
# 8. ADDITIONAL DATA CONSISTENCY
# --------------------------------

print("\nADDITIONAL DATA CONSISTENCY CHECKS")

invalid_starts = df[
    df["starts"] > df["appearances"]
]

print(
    f"Records where starts exceed appearances: "
    f"{len(invalid_starts)}"
)

invalid_minutes = df[
    (df["minutes"] < 0) |
    (df["minutes"] > df["appearances"] * 130)
]

print(
    f"Records with suspicious minutes: "
    f"{len(invalid_minutes)}"
)

# --------------------------------
# FINAL DATASET VALIDATION
# --------------------------------

print("\nFINAL DATASET VALIDATION")

# 1. Check duplicate player-season-competition records
duplicates = df.duplicated(
    subset=["player", "season", "competition", "team"]
)

print(f"Duplicate records: {duplicates.sum()}")
assert duplicates.sum() == 0, "Duplicate records found."


# 2. Check appearances and starts
invalid_starts = df[df["starts"] > df["appearances"]]

print(f"Invalid starts: {len(invalid_starts)}")
assert invalid_starts.empty, "Starts exceed appearances."


# 3. Check shooting statistics
shooting = df.dropna(
    subset=["shots_on_target", "shots_attempted"]
)

invalid_shooting = shooting[
    (shooting["shots_on_target"] > shooting["shots_attempted"])
    | (shooting["shots_on_target"] < 0)
    | (shooting["shots_attempted"] < 0)
]

print(f"Invalid shooting records: {len(invalid_shooting)}")
assert invalid_shooting.empty, "Invalid shooting statistics found."


# 4. Check passing statistics
passing = df.dropna(
    subset=["passes_completed", "passes_attempted"]
)

invalid_passing = passing[
    (passing["passes_completed"] > passing["passes_attempted"])
    | (passing["passes_completed"] < 0)
    | (passing["passes_attempted"] < 0)
]

print(f"Invalid passing records: {len(invalid_passing)}")
assert invalid_passing.empty, "Invalid passing statistics found."


# 5. Check supplied passing accuracy
accuracy_data = df.dropna(
    subset=[
        "passes_completed",
        "passes_attempted",
        "pass_accuracy"
    ]
)

calculated_accuracy = (
    accuracy_data["passes_completed"]
    / accuracy_data["passes_attempted"].replace(0, float("nan"))
) * 100

accuracy_difference = (
    calculated_accuracy - accuracy_data["pass_accuracy"]
).abs()

accuracy_mismatches = accuracy_data[
    accuracy_difference > 1.0
]

print(f"Passing accuracy mismatches: {len(accuracy_mismatches)}")

if not accuracy_mismatches.empty:
    print(
        accuracy_mismatches[
            [
                "player",
                "season",
                "competition",
                "passes_completed",
                "passes_attempted",
                "pass_accuracy"
            ]
        ].to_string(index=False)
    )


# 6. Report missing statistics by player
coverage_columns = [
    "shots_on_target",
    "shots_attempted",
    "passes_completed",
    "passes_attempted",
    "tackles",
    "interceptions"
]

print("\nSTATISTICAL DATA COVERAGE")

for player in sorted(df["player"].unique()):

    player_df = df[df["player"] == player]

    print(f"\n{player}")

    for column in coverage_columns:

        available = player_df[column].notna().sum()
        total = len(player_df)

        percentage = (available / total) * 100

        print(
            f"{column}: {available}/{total} "
            f"({percentage:.1f}%)"
        )


# 7. Check career goals against shooting-data coverage
print("\nGOAL COVERAGE")

for player in sorted(df["player"].unique()):

    player_df = df[df["player"] == player]

    total_goals = player_df["goals"].sum()

    complete_shooting = player_df.dropna(
        subset=["shots_on_target", "shots_attempted"]
    )

    represented_goals = complete_shooting["goals"].sum()

    coverage = (
        represented_goals / total_goals * 100
        if total_goals > 0
        else float("nan")
    )

    print(
        f"{player}: {represented_goals}/{total_goals} goals "
        f"represented ({coverage:.1f}%)"
    )


print("\nFINAL VALIDATION COMPLETED")
