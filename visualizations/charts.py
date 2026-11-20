
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# --------------------------------
# 1. GLOBAL CHART CONFIGURATION
# --------------------------------

PLAYER_COLORS = {
    "Pedri": "#E63946",
    "Jude Bellingham": "#457B9D"
}

DEFAULT_COLOR = "#7B8794"

CHART_TEMPLATE = "plotly_white"


def get_player_color(player):
    """Return a consistent colour for each player."""

    return PLAYER_COLORS.get(player, DEFAULT_COLOR)


def style_chart(
    fig,
    title=None,
    xaxis_title=None,
    yaxis_title=None,
    showlegend=False
):
    """Apply consistent styling across all charts."""

    fig.update_layout(
        template=CHART_TEMPLATE,
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(size=19)
        ),
        font=dict(
            family="Arial, sans-serif",
            size=12
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=showlegend,
        margin=dict(
            l=45,
            r=30,
            t=65,
            b=45
        ),
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E9ECEF",
        zeroline=False
    )

    return fig


def add_player_colors(fig):
    """Apply consistent player colours to chart traces."""

    for trace in fig.data:

        player = trace.name

        if player in PLAYER_COLORS:
            color = PLAYER_COLORS[player]
        else:
            color = DEFAULT_COLOR

        trace.marker.color = color

    return fig


# --------------------------------
# 2. GOALS
# --------------------------------

def create_goals_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="goals",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Career Goals Comparison",
        text="goals",
        labels={
            "player": "Player",
            "goals": "Total Goals"
        },
        hover_data={
            "goals": True
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Career Goals Comparison",
        xaxis_title="Player",
        yaxis_title="Goals"
    )

    return fig


# --------------------------------
# 3. ASSISTS
# --------------------------------

def create_assists_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="assists",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Career Assists Comparison",
        text="assists",
        labels={
            "player": "Player",
            "assists": "Total Assists"
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Career Assists Comparison",
        xaxis_title="Player",
        yaxis_title="Assists"
    )

    return fig


# --------------------------------
# 4. GOALS PER 90
# --------------------------------

def create_goals_per_90_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="goals_per_90",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Goals per 90 Minutes",
        text="goals_per_90",
        labels={
            "player": "Player",
            "goals_per_90": "Goals per 90"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Goals per 90 Minutes",
        xaxis_title="Player",
        yaxis_title="Goals per 90"
    )

    return fig


# --------------------------------
# 5. PASSING ACCURACY
# --------------------------------

def create_passing_accuracy_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="pass_accuracy",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Career Passing Accuracy",
        text="pass_accuracy",
        labels={
            "player": "Player",
            "pass_accuracy": "Passing Accuracy (%)"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Career Passing Accuracy",
        xaxis_title="Player",
        yaxis_title="Passing Accuracy (%)"
    )

    fig.update_yaxes(range=[0, 100])

    return fig


# --------------------------------
# 6. ASSISTS PER 90
# --------------------------------

def create_assists_per_90_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="assists_per_90",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Assists per 90 Minutes",
        text="assists_per_90",
        labels={
            "player": "Player",
            "assists_per_90": "Assists per 90"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Assists per 90 Minutes",
        xaxis_title="Player",
        yaxis_title="Assists per 90"
    )

    return fig


# --------------------------------
# 7. MINUTES PLAYED
# --------------------------------

def create_minutes_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="minutes",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Total Minutes Played",
        text="minutes",
        labels={
            "player": "Player",
            "minutes": "Minutes Played"
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Total Minutes Played",
        xaxis_title="Player",
        yaxis_title="Minutes"
    )

    return fig


# --------------------------------
# 8. TACKLES
# --------------------------------

def create_tackles_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="tackles",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Recorded Tackles Comparison",
        text="tackles",
        labels={
            "player": "Player",
            "tackles": "Recorded Tackles"
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Recorded Tackles Comparison",
        xaxis_title="Player",
        yaxis_title="Recorded Tackles"
    )

    return fig


# --------------------------------
# 9. INTERCEPTIONS
# --------------------------------

def create_interceptions_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="interceptions",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Recorded Interceptions Comparison",
        text="interceptions",
        labels={
            "player": "Player",
            "interceptions": "Recorded Interceptions"
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Recorded Interceptions Comparison",
        xaxis_title="Player",
        yaxis_title="Recorded Interceptions"
    )

    return fig


# --------------------------------
# 10. RADAR CHART
# --------------------------------

def create_radar_chart(df):

    metrics = [
        "Goals per 90",
        "Assists per 90",
        "Passing Accuracy"
    ]

    columns = [
        "goals_per_90",
        "assists_per_90",
        "pass_accuracy"
    ]

    # Reference values used to normalize the metrics.
    # These are comparison scales, not league averages.

    reference_values = [
        1.0,
        1.0,
        100
    ]

    fig = go.Figure()

    for _, player in df.iterrows():

        normalized_values = []

        for column, reference in zip(
            columns,
            reference_values
        ):

            value = player[column]

            if pd.isna(value):

                score = None

            else:

                score = max(
                    0,
                    min((value / reference) * 100, 100)
                )

            normalized_values.append(score)

        # Close the radar shape
        radar_values = normalized_values + [
            normalized_values[0]
        ]

        radar_metrics = metrics + [
            metrics[0]
        ]

        color = get_player_color(player["player"])

        fig.add_trace(
            go.Scatterpolar(
                r=radar_values,
                theta=radar_metrics,
                fill="toself",
                name=player["player"],
                line=dict(
                    color=color,
                    width=3
                ),
                opacity=0.75,
                connectgaps=False
            )
        )

    fig.update_layout(
        template=CHART_TEMPLATE,
        title=dict(
            text="Player Performance Profile",
            x=0.02,
            xanchor="left",
            font=dict(size=19)
        ),
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showline=False,
                gridcolor="#E9ECEF"
            ),
            angularaxis=dict(
                gridcolor="#E9ECEF"
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(
            l=60,
            r=60,
            t=70,
            b=70
        )
    )

    return fig


# --------------------------------
# 11. SHOT CONVERSION
# --------------------------------

def create_shot_conversion_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="shot_conversion_rate",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Shot Conversion Rate",
        labels={
            "player": "Player",
            "shot_conversion_rate": "Shot Conversion Rate (%)"
        },
        text="shot_conversion_rate"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Shot Conversion Rate",
        xaxis_title="Player",
        yaxis_title="Shot Conversion Rate (%)"
    )

    fig.update_yaxes(range=[0, 100])

    return fig


# --------------------------------
# 12. SHOTS ON TARGET
# --------------------------------

def create_shots_on_target_chart(df):

    fig = px.bar(
        df,
        x="player",
        y="shots_on_target_percentage",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        title="Shots on Target Percentage",
        labels={
            "player": "Player",
            "shots_on_target_percentage": "Shots on Target (%)"
        },
        text="shots_on_target_percentage"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False
    )

    style_chart(
        fig,
        title="Shots on Target Percentage",
        xaxis_title="Player",
        yaxis_title="Shots on Target (%)"
    )

    fig.update_yaxes(range=[0, 100])

    return fig


# --------------------------------
# 13. SEASONAL GOALS
# --------------------------------

def create_seasonal_goals_chart(df):

    fig = px.line(
        df,
        x="season",
        y="goals",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        markers=True,
        title="Goals Scored Per Season",
        labels={
            "season": "Season",
            "goals": "Goals",
            "player": "Player"
        }
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    style_chart(
        fig,
        title="Goals Scored Per Season",
        xaxis_title="Season",
        yaxis_title="Goals",
        showlegend=True
    )

    fig.update_layout(
        hovermode="x unified"
    )

    return fig


# --------------------------------
# 14. SEASONAL ASSISTS
# --------------------------------

def create_seasonal_assists_chart(df):

    fig = px.line(
        df,
        x="season",
        y="assists",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        markers=True,
        title="Assists Per Season",
        labels={
            "season": "Season",
            "assists": "Assists",
            "player": "Player"
        }
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    style_chart(
        fig,
        title="Assists Per Season",
        xaxis_title="Season",
        yaxis_title="Assists",
        showlegend=True
    )

    fig.update_layout(
        hovermode="x unified"
    )

    return fig


# --------------------------------
# 15. SEASONAL GOALS PER 90
# --------------------------------

def create_seasonal_goals_per_90_chart(df):

    fig = px.line(
        df,
        x="season",
        y="goals_per_90",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        markers=True,
        title="Goals Per 90 Minutes by Season",
        labels={
            "season": "Season",
            "goals_per_90": "Goals Per 90",
            "player": "Player"
        }
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    style_chart(
        fig,
        title="Goals Per 90 Minutes by Season",
        xaxis_title="Season",
        yaxis_title="Goals Per 90 Minutes",
        showlegend=True
    )

    fig.update_layout(
        hovermode="x unified"
    )

    return fig


# --------------------------------
# 16. SEASONAL ASSISTS PER 90
# --------------------------------

def create_seasonal_assists_per_90_chart(df):

    fig = px.line(
        df,
        x="season",
        y="assists_per_90",
        color="player",
        color_discrete_map=PLAYER_COLORS,
        markers=True,
        title="Assists Per 90 Minutes by Season",
        labels={
            "season": "Season",
            "assists_per_90": "Assists Per 90",
            "player": "Player"
        }
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    style_chart(
        fig,
        title="Assists Per 90 Minutes by Season",
        xaxis_title="Season",
        yaxis_title="Assists Per 90 Minutes",
        showlegend=True
    )

    fig.update_layout(
        hovermode="x unified"
    )

    return fig
