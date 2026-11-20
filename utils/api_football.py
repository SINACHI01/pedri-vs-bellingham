
import requests
import streamlit as st
import pandas as pd

BASE_URL = "https://v3.football.api-sports.io"


def get_api_data(endpoint, params=None):
    api_key = st.secrets["API_FOOTBALL_KEY"]

    url = f"{BASE_URL}/{endpoint}"

    headers = {
        "x-apisports-key": api_key
    }

    response = requests.get(
        url,
        headers=headers,
        params=params or {},
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise ValueError(f"API-Football error: {data['errors']}")

    return data.get("response", [])


def search_team(team_name):
    return get_api_data(
        "teams",
        {"search": team_name}
    )


def get_team_squad(team_id):
    return get_api_data(
        "players/squads",
        {"team": team_id}
    )



def get_player_seasons(player_id):
    return get_api_data(
        "players/seasons",
        {"player": player_id}
    )


def get_player_stats(player_id, season):
    return get_api_data(
        "players",
        {
            "id": player_id,
            "season": season
        }
    )


def flatten_player_stats(api_response):

    rows = []

    for player_record in api_response:

        player = player_record.get("player", {})

        for stat in player_record.get("statistics", []):

            games = stat.get("games") or {}
            goals = stat.get("goals") or {}
            shots = stat.get("shots") or {}
            passes = stat.get("passes") or {}
            tackles = stat.get("tackles") or {}
            dribbles = stat.get("dribbles") or {}

            row = {
                "player": player.get("name"),
                "team": stat.get("team", {}).get("name"),
                "team_id": stat.get("team", {}).get("id"),
                "competition": stat.get("league", {}).get("name"),
                "competition_id": stat.get("league", {}).get("id"),
                "season": stat.get("league", {}).get("season"),

                "appearances": games.get("appearences"),
                "starts": games.get("lineups"),
                "minutes": games.get("minutes"),

                "goals": goals.get("total"),
                "assists": goals.get("assists"),

                "total_shots": shots.get("total"),

                "passes_attempted": passes.get("total"),
                "pass_accuracy": passes.get("accuracy"),

                "tackles": tackles.get("total"),
                "interceptions": tackles.get("interceptions"),

                "dribbles_attempted": dribbles.get("attempts"),
                "dribbles_successful": dribbles.get("success")
            }

            rows.append(row)

    return pd.DataFrame(rows)
