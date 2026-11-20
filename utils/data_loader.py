
import pandas as pd
from pathlib import Path

from utils.api_football import (
    get_player_stats,
    flatten_player_stats
)


# Define the location of our CSV file
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "player_stats.csv"
)


def load_player_data(file_path=DATA_PATH):
    """
    Load football statistics from a CSV file.
    """

    try:
        df = pd.read_csv(file_path)
        return df

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find the data file: {file_path}"
        )

    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")

    except pd.errors.ParserError:
        raise ValueError("The CSV file could not be parsed.")


def inspect_player_data(df):

    print("\n--- FIRST FIVE ROWS ---")
    print(df.head())

    print("\n--- DATASET INFORMATION ---")
    print(df.info())

    print("\n--- DATASET SHAPE ---")
    print(df.shape)

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DUPLICATE ROWS ---")
    print(df.duplicated().sum())

    print("\n--- STATISTICAL SUMMARY ---")
    print(df.describe())


def clean_player_data(df):

    # Create a copy to protect the original dataset
    df = df.copy()

    # 1. Clean text columns
    text_columns = [
        "player",
        "season",
        "competition",
        "team"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    # 2. Identify numeric columns
    numeric_columns = [
        "appearances",
        "starts",
        "minutes",
        "goals",
        "assists",
        "shots_on_target",
        "shots_attempted",
        "passes_completed",
        "passes_attempted",
        "pass_accuracy",
        "key_passes",
        "tackles",
        "interceptions",
        "yellow_cards",
        "red_cards"
    ]

    # 3. Convert available columns to numeric types
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # 4. Remove rows without essential identification data
    df = df.dropna(
        subset=[
            "player",
            "season",
            "competition",
            "team"
        ]
    )

    # 5. Remove duplicate player-season-competition records
    df = df.drop_duplicates(
        subset=[
            "player",
            "season",
            "competition",
            "team"
        ]
    )

    # 6. Replace impossible negative statistics with missing values
    for column in numeric_columns:
        if column in df.columns:
            df.loc[
                df[column] < 0,
                column
            ] = float("nan")

    # 7. Validate passing accuracy
    if "pass_accuracy" in df.columns:
        df.loc[
            ~df["pass_accuracy"].between(0, 100),
            "pass_accuracy"
        ] = float("nan")

    # 8. Reset DataFrame index
    df = df.reset_index(drop=True)

    return df


def get_player_data(file_path=DATA_PATH):
    """
    Load and clean football statistics from CSV.
    """

    df = load_player_data(file_path)

    required_columns = [
        "player",
        "season",
        "competition",
        "team",
        "appearances",
        "starts",
        "minutes",
        "goals",
        "assists"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = clean_player_data(df)

    return df


def get_live_player_data(season=2024):
    """
    Retrieve real club statistics for Pedri and
    Jude Bellingham from API-Football.
    """

    players = {
        "Pedri": {
            "id": 133609,
            "club": "Barcelona"
        },
        "Jude Bellingham": {
            "id": 129718,
            "club": "Real Madrid"
        }
    }

    all_player_stats = []

    for player_name, details in players.items():

        # Retrieve statistics from API-Football
        api_response = get_player_stats(
            details["id"],
            season
        )

        if not api_response:
            continue

        # Convert API response into a DataFrame
        player_df = flatten_player_stats(api_response)

        # Keep club statistics only
        player_df = player_df[
            player_df["team"] == details["club"]
        ].copy()

        if player_df.empty:
            continue

        # Standardise player names
        player_df["player"] = player_name

        all_player_stats.append(player_df)

    if not all_player_stats:
        raise ValueError(
            f"No club statistics found for season {season}."
        )

    # Combine both players' statistics
    combined_df = pd.concat(
        all_player_stats,
        ignore_index=True
    )

    # Clean the API data
    combined_df = clean_player_data(combined_df)

    return combined_df
