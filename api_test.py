
import streamlit as st
import pandas as pd

from utils.api_football import (
    get_player_stats,
    flatten_player_stats
)

st.title("Pedri vs Jude Bellingham")

# API player IDs
players = {
    "Pedri": 133609,
    "Jude Bellingham": 129718
}

# Select the season
season = st.selectbox(
    "Select Season",
    [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    index=5
)

if st.button("Compare Players"):

    try:
        all_player_stats = []

        # Retrieve statistics for each player
        for player_name, player_id in players.items():

            stats = get_player_stats(player_id, season)

            if stats:

                # Convert API response into a DataFrame
                player_df = flatten_player_stats(stats)

                # Keep club statistics only
                club_name = (
                    "Barcelona"
                    if player_name == "Pedri"
                    else "Real Madrid"
                )

                player_df = player_df[
                    player_df["team"] == club_name
                ].copy()

                all_player_stats.append(player_df)

                st.success(
                    f"{player_name}: Statistics retrieved successfully"
                )

            else:
                st.warning(
                    f"No statistics found for {player_name} "
                    f"in {season}"
                )

        # Combine both players' statistics
        if all_player_stats:

            comparison_df = pd.concat(
                all_player_stats,
                ignore_index=True
            )

            st.subheader(
                f"Player Statistics - {season}"
            )

            st.dataframe(
                comparison_df,
                use_container_width=True
            )

        else:
            st.warning("No player statistics were retrieved.")

    except Exception as error:
        st.error(f"Error: {error}")
