
import pandas as pd


# --------------------------------
# 1. CAREER TOTALS
# --------------------------------

def calculate_career_totals(df):
    """Calculate career totals while preserving unavailable statistics."""

    general_columns = [
        "appearances",
        "starts",
        "minutes",
        "goals",
        "assists",
        "tackles",
        "interceptions",
        "yellow_cards",
        "red_cards"
    ]

    career_totals = (
        df.groupby("player")[general_columns]
        .sum(min_count=1)
        .reset_index()
    )

    # Shooting statistics: only records with complete shot data
    shooting_df = df.dropna(
        subset=["goals", "shots_on_target", "shots_attempted"]
    )

    shooting_totals = (
        shooting_df.groupby("player")
        .agg(
            shooting_goals=("goals", "sum"),
            shots_on_target=("shots_on_target", "sum"),
            shots_attempted=("shots_attempted", "sum")
        )
        .reset_index()
    )

    career_totals = career_totals.merge(
        shooting_totals,
        on="player",
        how="left"
    )

    # Passing statistics: only records with both values available
    passing_df = df.dropna(
        subset=["passes_completed", "passes_attempted"]
    )

    passing_totals = (
        passing_df.groupby("player")
        .agg(
            passes_completed=("passes_completed", "sum"),
            passes_attempted=("passes_attempted", "sum")
        )
        .reset_index()
    )

    career_totals = career_totals.merge(
        passing_totals,
        on="player",
        how="left"
    )

    return career_totals


# --------------------------------
# 2. PER-90 STATISTICS
# --------------------------------

def calculate_per_90(career_totals):
    """Calculate player statistics per 90 minutes."""

    career_totals = career_totals.copy()

    minutes = career_totals["minutes"].replace(
        0, float("nan")
    )

    career_totals["goals_per_90"] = (
        career_totals["goals"] / minutes
    ) * 90

    career_totals["assists_per_90"] = (
        career_totals["assists"] / minutes
    ) * 90

    career_totals["tackles_per_90"] = (
        career_totals["tackles"] / minutes
    ) * 90

    career_totals["interceptions_per_90"] = (
        career_totals["interceptions"] / minutes
    ) * 90

    return career_totals


# --------------------------------
# 3. PASSING ACCURACY
# --------------------------------

def calculate_passing_accuracy(career_totals):
    """Calculate passing accuracy from completed and attempted passes."""

    career_totals = career_totals.copy()

    career_totals["pass_accuracy"] = (
        career_totals["passes_completed"] /
        career_totals["passes_attempted"].replace(
            0, float("nan")
        )
    ) * 100

    return career_totals


# --------------------------------
# 4. SHOT CONVERSION RATE
# --------------------------------

def calculate_shot_conversion_rate(career_totals):
    """Calculate the percentage of shots converted into goals."""

    career_totals = career_totals.copy()

    career_totals["shot_conversion_rate"] = (
        career_totals["shooting_goals"] /
        career_totals["shots_attempted"].replace(
            0, float("nan")
        )
    ) * 100

    return career_totals


# --------------------------------
# 5. SHOTS ON TARGET PERCENTAGE
# --------------------------------

def calculate_shots_on_target_percentage(career_totals):
    """Calculate the percentage of attempts on target."""

    career_totals = career_totals.copy()

    career_totals["shots_on_target_percentage"] = (
        career_totals["shots_on_target"] /
        career_totals["shots_attempted"].replace(
            0, float("nan")
        )
    ) * 100

    return career_totals


# --------------------------------
# 6. BUILD PLAYER COMPARISON TABLE
# --------------------------------

def build_comparison_table(df):
    """Build the career comparison table for selected players."""

    career_totals = calculate_career_totals(df)

    career_stats = calculate_per_90(career_totals)
    career_stats = calculate_passing_accuracy(career_stats)
    career_stats = calculate_shot_conversion_rate(career_stats)

    career_stats = calculate_shots_on_target_percentage(
        career_stats
    )

    comparison_columns = [
        "player",
        "appearances",
        "starts",
        "minutes",
        "goals",
        "assists",
        "shooting_goals",
        "shots_on_target",
        "shots_attempted",
        "goals_per_90",
        "assists_per_90",
        "pass_accuracy",
        "shot_conversion_rate",
        "shots_on_target_percentage",
        "tackles",
        "interceptions",
        "tackles_per_90",
        "interceptions_per_90"
    ]

    comparison_table = career_stats[
        comparison_columns
    ].copy()

    return comparison_table.round(2)


# --------------------------------
# 7. SEASONAL STATISTICS
# --------------------------------

def calculate_seasonal_stats(df):
    """Calculate player statistics for each season."""

    seasonal_columns = [
        "appearances",
        "minutes",
        "goals",
        "assists"
    ]

    seasonal_stats = (
        df.groupby(["player", "season"])[seasonal_columns]
        .sum(min_count=1)
        .reset_index()
    )

    minutes = seasonal_stats["minutes"].replace(
        0, float("nan")
    )

    seasonal_stats["goals_per_90"] = (
        seasonal_stats["goals"] / minutes
    ) * 90

    seasonal_stats["assists_per_90"] = (
        seasonal_stats["assists"] / minutes
    ) * 90

    return seasonal_stats


# --------------------------------
# 8. PLAYER PERFORMANCE INSIGHTS
# --------------------------------

def generate_player_insights(df):
    """Generate natural-language comparisons for two players."""

    if df["player"].nunique() != 2:
        return [
            "Select exactly two players to generate performance insights."
        ]

    metrics = {
        "goals": "goals",
        "assists": "assists",
        "goals_per_90": "goals per 90 minutes",
        "pass_accuracy": "passing accuracy",
        "shot_conversion_rate": "shot conversion rate",
        "tackles_per_90": "tackles per 90 minutes",
        "interceptions_per_90": "interceptions per 90 minutes"
    }

    insights = []

    players = df["player"].drop_duplicates().tolist()
    player_one, player_two = players

    values = df.set_index("player")

    for metric, label in metrics.items():

        value_one = values.loc[player_one, metric]
        value_two = values.loc[player_two, metric]

        if pd.isna(value_one) or pd.isna(value_two):

            insights.append(
                f"Insufficient data to compare {label}."
            )

        elif value_one > value_two:

            insights.append(
                f"{player_one} leads in {label}."
            )

        elif value_two > value_one:

            insights.append(
                f"{player_two} leads in {label}."
            )

        else:

            insights.append(
                f"Both players are tied in {label}."
            )

    return insights


# --------------------------------
# 9. PLAYER STRENGTHS & WEAKNESSES
# --------------------------------

def generate_player_strengths_weaknesses(df):
    """Identify relative statistical advantages for two players."""

    if df["player"].nunique() != 2:
        return {}

    metrics = {
        "goals": "Goals",
        "assists": "Assists",
        "goals_per_90": "Goals per 90",
        "pass_accuracy": "Passing accuracy",
        "shot_conversion_rate": "Shot conversion rate",
        "tackles_per_90": "Tackles per 90",
        "interceptions_per_90": "Interceptions per 90"
    }

    players = df["player"].drop_duplicates().tolist()

    results = {
        player: {
            "strengths": [],
            "weaknesses": [],
            "insufficient_data": []
        }
        for player in players
    }

    values = df.set_index("player")

    player_one = players[0]
    player_two = players[1]

    for metric, label in metrics.items():

        value_one = values.loc[player_one, metric]
        value_two = values.loc[player_two, metric]

        if pd.isna(value_one) or pd.isna(value_two):

            for player in players:
                results[player]["insufficient_data"].append(label)

        elif value_one > value_two:

            results[player_one]["strengths"].append(label)
            results[player_two]["weaknesses"].append(label)

        elif value_two > value_one:

            results[player_two]["strengths"].append(label)
            results[player_one]["weaknesses"].append(label)

    return results
