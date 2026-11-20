
import streamlit as st
import pandas as pd

from utils.data_loader import get_player_data

st.set_page_config(
    page_title="Football Dataset Validation",
    layout="wide"
)

st.title("Football Dataset Validation")

try:
    # Load and clean the CSV dataset
    df = get_player_data()

    st.success("Dataset loaded successfully!")

    # 1. Dataset Overview
    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))
    col2.metric("Players", df["player"].nunique())
    col3.metric("Competitions", df["competition"].nunique())

    # 2. Player Distribution
    st.subheader("Player Distribution")
    st.dataframe(
        df["player"].value_counts().rename("Records"),
        use_container_width=True
    )

    # 3. Available Seasons
    st.subheader("Seasons")
    st.write(sorted(df["season"].unique()))

    # 4. Missing Values
    st.subheader("Missing Values")

    missing_values = df.isnull().sum()

    st.dataframe(
        missing_values.rename("Missing Values"),
        use_container_width=True
    )

    # 5. Duplicate Records
    st.subheader("Duplicate Records")

    duplicate_count = df.duplicated().sum()
    st.metric("Duplicate Rows", duplicate_count)

    # 6. Data Types
    st.subheader("Data Types")

    st.dataframe(
        df.dtypes.astype(str).rename("Data Type"),
        use_container_width=True
    )

    # 7. Shooting Data Consistency
    st.subheader("Shooting Data Consistency")

    shot_data = df[
        [
            "player",
            "season",
            "competition",
            "shots_on_target",
            "shots_attempted"
        ]
    ].dropna(
        subset=["shots_on_target", "shots_attempted"]
    )

    invalid_shots = shot_data[
        shot_data["shots_on_target"] > shot_data["shots_attempted"]
    ]

    col1, col2 = st.columns(2)

    col1.metric("Records With Shooting Data", len(shot_data))
    col2.metric("Invalid Shooting Records", len(invalid_shots))

    if invalid_shots.empty:
        st.success("All available shooting records are consistent.")
    else:
        st.error("Some shooting records need investigation.")
        st.dataframe(
            invalid_shots,
            use_container_width=True
        )

    # 8. Passing Data Consistency
    st.subheader("Passing Data Consistency")

    passing_data = df.dropna(
        subset=["passes_completed", "passes_attempted"]
    )

    invalid_passes = passing_data[
        passing_data["passes_completed"] > passing_data["passes_attempted"]
    ]

    if invalid_passes.empty:
        st.success("All available passing records are consistent.")
    else:
        st.error("Some passing records need investigation.")
        st.dataframe(
            invalid_passes[
                [
                    "player",
                    "season",
                    "competition",
                    "passes_completed",
                    "passes_attempted"
                ]
            ],
            use_container_width=True
        )

    # 9. Complete Dataset
    st.subheader("Complete Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as error:
    st.error(f"Validation failed: {error}")
