
import re
from datetime import date
from pathlib import Path

import streamlit as st
import pandas as pd

from visualizations.charts import (
    create_goals_chart,
    create_assists_chart,
    create_goals_per_90_chart,
    create_passing_accuracy_chart,
    create_assists_per_90_chart,
    create_minutes_chart,
    create_tackles_chart,
    create_interceptions_chart,
    create_radar_chart,
    create_shot_conversion_chart,
    create_shots_on_target_chart,
    create_seasonal_goals_chart,
    create_seasonal_assists_chart,
    create_seasonal_goals_per_90_chart,
    create_seasonal_assists_per_90_chart
)

from utils.data_loader import get_player_data

from utils.calculations import (
    build_comparison_table,
    calculate_seasonal_stats,
    generate_player_insights,
    generate_player_strengths_weaknesses
)


# --------------------------------
# PLAYER PROFILE INFORMATION
# --------------------------------

PLAYER_PROFILES = {
    "Pedri": {
        "nationality": "Spanish",
        "position": "Midfielder",
        "date_of_birth": "2002-11-25"
    },

    "Jude Bellingham": {
        "nationality": "English",
        "position": "Midfielder",
        "date_of_birth": "2003-06-29"
    }
}


# --------------------------------
# PLAYER PROFILE IMAGES
# --------------------------------

ASSETS_DIR = Path(__file__).parent / "assets"

PLAYER_IMAGES = {
    "Pedri": ASSETS_DIR / "pedri.jpg",
    "Jude Bellingham": ASSETS_DIR / "jude_bellingham.jpg"
}


# --------------------------------
# HELPER FUNCTIONS
# --------------------------------

def format_metric(value, suffix="", decimals=2):
    """Format metrics safely, displaying N/A for missing values."""

    if pd.isna(value):
        return "N/A"

    return f"{value:.{decimals}f}{suffix}"


def get_metric_leader(df, metric):
    """Identify the player leading a metric, including ties."""

    valid_data = df.dropna(subset=[metric])

    if valid_data.empty:
        return "N/A"

    highest_value = valid_data[metric].max()

    leaders = valid_data.loc[
        valid_data[metric] == highest_value,
        "player"
    ].tolist()

    if len(leaders) > 1:
        return f"Tie: {', '.join(leaders)}"

    return leaders[0]


def calculate_age(date_of_birth):
    """Calculate a player's current age from their date of birth."""

    birth_date = date.fromisoformat(date_of_birth)
    today = date.today()

    age = today.year - birth_date.year

    if (today.month, today.day) < (
        birth_date.month,
        birth_date.day
    ):
        age -= 1

    return age


def get_season_start_year(season):
    """Extract the starting year from a season label."""

    match = re.search(r"\d{4}", str(season))

    if match:
        return int(match.group())

    return 0


def get_player_profile_data(df, player):
    """
    Retrieve profile information and dataset-specific details.

    Team and season information come from the CSV dataset.
    """

    player_df = df[df["player"] == player].copy()

    profile = PLAYER_PROFILES.get(player, {})

    nationality = profile.get("nationality", "Not available")
    position = profile.get("position", "Not available")
    date_of_birth = profile.get("date_of_birth")

    age = (
        calculate_age(date_of_birth)
        if date_of_birth
        else None
    )

    # Use club records to identify the latest club represented.
    if "team_type" in player_df.columns:

        club_records = player_df[
            player_df["team_type"] == "Club"
        ].copy()

    else:

        club_records = player_df.copy()

    if not club_records.empty:

        club_records["season_year"] = (
            club_records["season"].apply(get_season_start_year)
        )

        latest_year = club_records["season_year"].max()

        latest_records = club_records[
            club_records["season_year"] == latest_year
        ]

        latest_teams = sorted(
            latest_records["team"].dropna().unique().tolist()
        )

        latest_team = ", ".join(latest_teams) if latest_teams else "N/A"

    else:

        latest_team = "N/A"

    seasons = sorted(
        player_df["season"].dropna().unique().tolist(),
        key=get_season_start_year
    )

    number_of_seasons = len(seasons)

    if seasons:

        if len(seasons) == 1:
            season_range = seasons[0]

        else:
            season_range = f"{seasons[0]} – {seasons[-1]}"

    else:

        season_range = "N/A"

    return {
        "nationality": nationality,
        "position": position,
        "age": age,
        "date_of_birth": date_of_birth,
        "latest_team": latest_team,
        "number_of_seasons": number_of_seasons,
        "season_range": season_range
    }


# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Football Player Comparison",
    page_icon="⚽",
    layout="wide"
)


# --------------------------------
# 2. DASHBOARD TITLE
# --------------------------------

st.title("⚽ Football Player Comparison")

st.subheader(
    "Compare football players using career statistics"
)

st.caption(
    "A statistical comparison of player performance across "
    "club and international competitions."
)

st.divider()


# --------------------------------
# 3. LOAD FOOTBALL DATA
# --------------------------------

try:

    df = get_player_data()

    st.success("Football statistics loaded successfully!")

    # --------------------------------
    # 4. DATA FILTERS
    # --------------------------------

    st.sidebar.header("Data Filters")

    international_teams = ["Spain", "England"]

    df["team_type"] = df["team"].isin(
        international_teams
    ).map({
        True: "International",
        False: "Club"
    })

    selected_team_type = st.sidebar.selectbox(
        "Select Competition Type",
        options=[
            "All",
            "Club",
            "International"
        ]
    )

    seasons = sorted(
        df["season"].dropna().unique(),
        reverse=True
    )

    selected_season = st.sidebar.selectbox(
        "Select Season",
        options=["All Seasons"] + list(seasons)
    )

    competitions = sorted(
        df["competition"].dropna().unique()
    )

    selected_competition = st.sidebar.selectbox(
        "Select Competition",
        options=["All Competitions"] + list(competitions)
    )

    # --------------------------------
    # 5. APPLY FILTERS
    # --------------------------------

    filtered_df = df.copy()

    if selected_team_type != "All":

        filtered_df = filtered_df[
            filtered_df["team_type"] == selected_team_type
        ]

    if selected_season != "All Seasons":

        filtered_df = filtered_df[
            filtered_df["season"] == selected_season
        ]

    if selected_competition != "All Competitions":

        filtered_df = filtered_df[
            filtered_df["competition"] == selected_competition
        ]

    if filtered_df.empty:

        st.warning(
            "No records match the selected filters. "
            "Please change your filter selections."
        )

        st.stop()

    # --------------------------------
    # 6. CALCULATE COMPARISON STATISTICS
    # --------------------------------

    comparison = build_comparison_table(filtered_df)

    st.caption(
        f"Showing statistics for: "
        f"{selected_team_type} | "
        f"{selected_season} | "
        f"{selected_competition}"
    )

    # --------------------------------
    # 7. PLAYER SELECTION
    # --------------------------------

    st.sidebar.header("Player Selection")

    players = sorted(comparison["player"].unique())

    selected_players = st.sidebar.multiselect(
        "Select players to compare",
        options=players,
        default=players[:2]
    )

    if not selected_players:

        st.warning("Please select at least one player.")

    else:

        # --------------------------------
        # 8. FILTER SELECTED PLAYERS
        # --------------------------------

        selected_data = comparison[
            comparison["player"].isin(selected_players)
        ].copy()

        # --------------------------------
        # 8A. PLAYER PROFILE CARDS
        # --------------------------------

        st.header("Player Profiles")

        st.caption(
            "Basic player information alongside the seasons "
            "represented in your dataset."
        )

        profile_columns = st.columns(len(selected_players))

        for column, player in zip(
            profile_columns,
            selected_players
        ):

            profile = get_player_profile_data(df, player)

            with column:

                with st.container(border=True):

                    # Player photograph
                    image_path = PLAYER_IMAGES.get(player)

                    if image_path and image_path.exists():

                        st.image(
                            str(image_path),
                            width=220
                        )

                    else:

                        st.warning(
                            f"Image not found for {player}. "
                            "Check the assets folder."
                        )

                    st.subheader(player)

                    st.markdown(
                        f"**{profile['nationality']}** · "
                        f"{profile['position']}"
                    )

                    st.divider()

                    age_display = (
                        f"{profile['age']} years"
                        if profile["age"] is not None
                        else "N/A"
                    )

                    st.metric(
                        "Age",
                        age_display
                    )

                    st.metric(
                        "Latest Club in Dataset",
                        profile["latest_team"]
                    )

                    st.metric(
                        "Seasons Represented",
                        profile["number_of_seasons"]
                    )

                    st.caption(
                        f"Dataset coverage: {profile['season_range']}"
                    )

                    if profile["date_of_birth"]:

                        st.caption(
                            f"Date of birth: {profile['date_of_birth']}"
                        )

        st.divider()

        # --------------------------------
        # 9. DISPLAY PLAYER METRICS
        # --------------------------------

        st.header("Player Statistics")

        columns = st.columns(len(selected_players))

        for column, player in zip(columns, selected_players):

            player_stats = selected_data[
                selected_data["player"] == player
            ].iloc[0]

            with column:

                st.subheader(player)

                st.metric(
                    "Appearances",
                    format_metric(
                        player_stats["appearances"],
                        decimals=0
                    )
                )

                st.metric(
                    "Goals",
                    format_metric(
                        player_stats["goals"],
                        decimals=0
                    )
                )

                st.metric(
                    "Assists",
                    format_metric(
                        player_stats["assists"],
                        decimals=0
                    )
                )

                st.metric(
                    "Goals per 90",
                    format_metric(
                        player_stats["goals_per_90"]
                    )
                )

                st.metric(
                    "Assists per 90",
                    format_metric(
                        player_stats["assists_per_90"]
                    )
                )

                st.metric(
                    "Passing Accuracy",
                    format_metric(
                        player_stats["pass_accuracy"],
                        suffix="%"
                    )
                )

        # --------------------------------
        # 9B. HEAD-TO-HEAD LEADERS
        # --------------------------------

        st.divider()

        st.header("Head-to-Head Leaders")

        st.caption(
            "See which selected player leads in each statistical category."
        )

        leader_col1, leader_col2 = st.columns(2)

        with leader_col1:

            st.metric(
                "Goals Leader",
                get_metric_leader(selected_data, "goals")
            )

            st.metric(
                "Goals per 90 Leader",
                get_metric_leader(selected_data, "goals_per_90")
            )

        with leader_col2:

            st.metric(
                "Assists Leader",
                get_metric_leader(selected_data, "assists")
            )

            st.metric(
                "Passing Accuracy Leader",
                get_metric_leader(selected_data, "pass_accuracy")
            )

        # --------------------------------
        # 9C. PLAYER PERFORMANCE INSIGHTS
        # --------------------------------

        st.divider()

        st.header("Player Performance Insights")

        st.caption(
            "Automatically generated insights based on the "
            "selected players' statistics."
        )

        insights = generate_player_insights(selected_data)

        for insight in insights:
            st.info(insight)

        # --------------------------------
        # 9D. DATA COVERAGE & RELIABILITY
        # --------------------------------

        st.divider()

        st.header("Data Coverage & Reliability")

        st.caption(
            "Shows how much of each player's available dataset "
            "contains the statistics required for each comparison. "
            "Coverage changes with the selected filters."
        )

        coverage_records = []

        for player in selected_players:

            player_df = filtered_df[
                filtered_df["player"] == player
            ].copy()

            total_records = len(player_df)

            shooting_records = player_df.dropna(
                subset=[
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

            total_goals = player_df["goals"].sum()

            represented_goals = shooting_records["goals"].sum()

            goal_coverage = (
                (represented_goals / total_goals) * 100
                if total_goals > 0
                else 0
            )

            coverage_records.append({
                "Player": player,
                "Total Records": total_records,

                "Shooting Records": (
                    f"{len(shooting_records)}/{total_records} "
                    f"({len(shooting_records) / total_records * 100:.1f}%)"
                    if total_records else "N/A"
                ),

                "Passing Records": (
                    f"{len(passing_records)}/{total_records} "
                    f"({len(passing_records) / total_records * 100:.1f}%)"
                    if total_records else "N/A"
                ),

                "Defensive Records": (
                    f"{len(defensive_records)}/{total_records} "
                    f"({len(defensive_records) / total_records * 100:.1f}%)"
                    if total_records else "N/A"
                ),

                "Goals Represented": (
                    f"{represented_goals:.0f}/{total_goals:.0f} "
                    f"({goal_coverage:.1f}%)"
                )
            })

        coverage_df = pd.DataFrame(coverage_records)

        st.dataframe(
            coverage_df,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Important: Missing statistics are treated as unavailable, "
            "not as zero. Shooting, passing and defensive comparisons "
            "are based only on records with the required data available."
        )

        # --------------------------------
        # 9E. PLAYER STRENGTHS & WEAKNESSES
        # --------------------------------

        st.divider()

        st.header("Player Strengths & Weaknesses")

        st.caption(
            "A relative comparison of each player's statistical "
            "advantages and disadvantages."
        )

        strengths_weaknesses = generate_player_strengths_weaknesses(
            selected_data
        )

        if len(strengths_weaknesses) == 2:

            player_columns = st.columns(2)

            for column, (player, analysis) in zip(
                player_columns,
                strengths_weaknesses.items()
            ):

                with column:

                    st.subheader(player)

                    st.markdown("**Strengths**")

                    if analysis["strengths"]:

                        for strength in analysis["strengths"]:
                            st.success(f"✓ {strength}")

                    else:

                        st.write("No relative strengths identified.")

                    st.markdown("**Weaknesses**")

                    if analysis["weaknesses"]:

                        for weakness in analysis["weaknesses"]:
                            st.warning(f"• {weakness}")

                    else:

                        st.write("No relative weaknesses identified.")

                    if analysis["insufficient_data"]:

                        st.markdown("**Insufficient Data**")

                        for metric in analysis["insufficient_data"]:
                            st.info(metric)

        else:

            st.info(
                "Select exactly two players to view their "
                "strengths and weaknesses."
            )

        # --------------------------------
        # 10. DISPLAY COMPARISON TABLE
        # --------------------------------

        st.divider()

        st.header("Statistical Comparison")

        st.dataframe(
            selected_data,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------
        # DOWNLOAD CAREER COMPARISON DATA
        # --------------------------------

        csv_data = selected_data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Career Statistics (CSV)",
            data=csv_data,
            file_name="football_player_comparison.csv",
            mime="text/csv"
        )

        # --------------------------------
        # 11. DASHBOARD TABS
        # --------------------------------

        overview_tab, attacking_tab, passing_tab, defensive_tab = st.tabs(
            [
                "Overview",
                "Attacking",
                "Passing",
                "Defensive"
            ]
        )

        # --------------------------------
        # 12. OVERVIEW TAB
        # --------------------------------

        with overview_tab:

            st.header("Player Comparison")

            st.dataframe(
                selected_data,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("Overall Performance Profile")

            radar_fig = create_radar_chart(selected_data)

            st.plotly_chart(
                radar_fig,
                use_container_width=True
            )

        # --------------------------------
        # 13. ATTACKING TAB
        # --------------------------------

        with attacking_tab:

            st.header("Attacking Performance")

            col1, col2 = st.columns(2)

            with col1:

                st.plotly_chart(
                    create_goals_chart(selected_data),
                    use_container_width=True
                )

            with col2:

                st.plotly_chart(
                    create_assists_chart(selected_data),
                    use_container_width=True
                )

            col3, col4 = st.columns(2)

            with col3:

                st.plotly_chart(
                    create_goals_per_90_chart(selected_data),
                    use_container_width=True
                )

            with col4:

                st.plotly_chart(
                    create_assists_per_90_chart(selected_data),
                    use_container_width=True
                )

            st.divider()

            st.subheader("Shooting Statistics")

            col5, col6 = st.columns(2)

            with col5:

                st.plotly_chart(
                    create_shot_conversion_chart(selected_data),
                    use_container_width=True
                )

            with col6:

                st.plotly_chart(
                    create_shots_on_target_chart(selected_data),
                    use_container_width=True
                )

        # --------------------------------
        # 14. PASSING TAB
        # --------------------------------

        with passing_tab:

            st.header("Passing Performance")

            st.plotly_chart(
                create_passing_accuracy_chart(selected_data),
                use_container_width=True
            )

        # --------------------------------
        # 15. DEFENSIVE TAB
        # --------------------------------

        with defensive_tab:

            st.header("Defensive Performance")

            col7, col8 = st.columns(2)

            with col7:

                st.plotly_chart(
                    create_tackles_chart(selected_data),
                    use_container_width=True
                )

            with col8:

                st.plotly_chart(
                    create_interceptions_chart(selected_data),
                    use_container_width=True
                )

        # --------------------------------
        # 16. PLAYING TIME
        # --------------------------------

        st.divider()

        st.header("Playing Time")

        st.plotly_chart(
            create_minutes_chart(selected_data),
            use_container_width=True
        )

        # --------------------------------
        # 17. SEASON-BY-SEASON PERFORMANCE
        # --------------------------------

        st.divider()

        st.header("Season-by-Season Performance")

        seasonal_stats = calculate_seasonal_stats(filtered_df)

        seasonal_stats = seasonal_stats[
            seasonal_stats["player"].isin(selected_players)
        ]

        # --------------------------------
        # SEASONAL STATISTICS TABLE
        # --------------------------------

        st.divider()

        st.subheader("Seasonal Statistics Summary")

        seasonal_table = seasonal_stats[
            [
                "player",
                "season",
                "appearances",
                "minutes",
                "goals",
                "assists",
                "goals_per_90",
                "assists_per_90"
            ]
        ].copy()

        seasonal_table = seasonal_table.round(2)

        st.dataframe(
            seasonal_table,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------
        # DOWNLOAD SEASONAL STATISTICS
        # --------------------------------

        seasonal_csv = seasonal_table.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Seasonal Statistics (CSV)",
            data=seasonal_csv,
            file_name="football_seasonal_statistics.csv",
            mime="text/csv"
        )

        # Goals and assists totals
        col9, col10 = st.columns(2)

        with col9:

            st.plotly_chart(
                create_seasonal_goals_chart(seasonal_stats),
                use_container_width=True
            )

        with col10:

            st.plotly_chart(
                create_seasonal_assists_chart(seasonal_stats),
                use_container_width=True
            )

        # Seasonal efficiency
        st.divider()

        st.subheader("Seasonal Efficiency")

        col11, col12 = st.columns(2)

        with col11:

            st.plotly_chart(
                create_seasonal_goals_per_90_chart(seasonal_stats),
                use_container_width=True
            )

        with col12:

            st.plotly_chart(
                create_seasonal_assists_per_90_chart(seasonal_stats),
                use_container_width=True
            )


except (FileNotFoundError, ValueError, KeyError) as e:

    st.error(f"Unable to load football data: {e}")
