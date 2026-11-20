# ⚽ Pedri vs Jude Bellingham — Football Analytics Dashboard

An interactive football analytics dashboard built with **Python, Streamlit, Pandas, and Plotly**, designed to compare the performance of two of Europe's most exciting midfielders: **Pedri** and **Jude Bellingham**.

Explore their statistics, compare key performance metrics, identify strengths and weaknesses, and analyse their performances across different seasons and competitions.

## 🚀 Live Demo

**[View the Live Dashboard](https://pedri-vs-bellingham-gkm27jshqnumwqyry8zkhb.streamlit.app/)**

## 📌 Project Overview

This project explores how data analytics can be used to evaluate and compare football players beyond traditional statistics.

Rather than relying solely on goals and assists, the dashboard examines multiple aspects of player performance, including attacking contributions, passing, defensive actions, and playing time.

The goal is to provide an interactive, data-driven comparison that makes football statistics easier to explore, interpret, and understand.

## ✨ Key Features

### 1. Player Profiles

- Individual profiles for Pedri and Jude Bellingham.
- Player images, nationality, position, and age.
- Latest available club and statistical coverage information.

### 2. Head-to-Head Comparison

- Compare key performance metrics between both players.
- Identify statistical leaders across selected metrics.
- Explore differences in attacking and overall contributions.

### 3. Attacking Analysis

- Goals and assists.
- Goals per 90 minutes.
- Assists per 90 minutes.
- Shots attempted and shots on target.
- Shot conversion.
- Seasonal attacking performance trends.

### 4. Passing Analysis

- Completed and attempted passes.
- Passing accuracy.
- Key passes.
- Comparative passing performance.

### 5. Defensive Analysis

- Recorded tackles.
- Recorded interceptions.
- Defensive statistics comparison.

### 6. Performance Visualizations

Interactive charts built with Plotly, including:

- Bar charts.
- Seasonal performance charts.
- Radar charts.
- Comparative statistical visualizations.

### 7. Data Exploration

- Filter statistics by player, season, and competition.
- Explore detailed seasonal statistics.
- View data coverage and availability.
- Download comparison data as CSV files.

## 🛠️ Technology Stack

| Technology                | Purpose                                   |
| ------------------------- | ----------------------------------------- |
| Python                    | Core programming language                 |
| Streamlit                 | Interactive dashboard and web application |
| Pandas                    | Data manipulation and analysis            |
| NumPy                     | Numerical computations                    |
| Plotly                    | Interactive data visualizations           |
| Git & GitHub              | Version control and project hosting       |
| Streamlit Community Cloud | Application deployment                    |

## 📂 Project Structure

```text
pedri-vs-bellingham/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   ├── pedri.jpg
│   └── jude_bellingham.jpg
│
├── data/
│   └── raw/
│       └── player_stats.csv
│
├── utils/
│   ├── __init__.py
│   ├── api_football.py
│   ├── data_loader.py
│   └── calculations.py
│
├── visualizations/
│   └── charts.py
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── test files
```

## 📊 Dataset

The project uses a curated CSV dataset as its primary data source.

The dataset contains player statistics across multiple seasons and competitions, covering the 2019/20 to 2026/27 period.

### Dataset columns

| Column           | Description             |
| ---------------- | ----------------------- |
| player           | Player name             |
| season           | Season or calendar year |
| competition      | Competition played      |
| team             | Team represented        |
| appearances      | Total appearances       |
| starts           | Starting appearances    |
| minutes          | Minutes played          |
| goals            | Goals scored            |
| assists          | Assists recorded        |
| shots_on_target  | Shots on target         |
| shots_attempted  | Total shots attempted   |
| passes_completed | Completed passes        |
| passes_attempted | Total passes attempted  |
| pass_accuracy    | Passing accuracy        |
| key_passes       | Key passes              |
| tackles          | Tackles recorded        |
| interceptions    | Interceptions recorded  |
| yellow_cards     | Yellow cards            |
| red_cards        | Red cards               |

**Data quality considerations:**

- Missing values represent unavailable or unreported statistics, not necessarily zero.
- Some competitions have more complete statistical coverage than others.
- Defensive statistics may have limited coverage.
- Club seasons and international calendar-year records are represented differently.

The dashboard accounts for data availability when presenting comparisons. Statistical conclusions should therefore be interpreted in the context of the available records.

## 📈 Statistical Approach

The dashboard uses several performance indicators to support comparisons.

**Per 90-minute metrics**

These help account for differences in playing time:

\[
\text{Metric per 90} =
\frac{\text{Total Metric}}{\text{Minutes Played}} \times 90
\]

**Passing accuracy**

\[
\text{Passing Accuracy} =
\frac{\text{Passes Completed}}{\text{Passes Attempted}} \times 100
\]

**Shot conversion**

\[
\text{Shot Conversion} =
\frac{\text{Goals}}{\text{Shots Attempted}} \times 100
\]

These metrics provide additional context beyond raw totals.

## 💻 Run Locally

Want to explore or modify the project?

### Prerequisites

- Python 3.12 or compatible version.
- Git.
- Visual Studio Code or another Python IDE.

### 1. Clone the repository

```bash
git clone https://github.com/SINACHI01/pedri-vs-bellingham.git
```

### 2. Navigate into the project

```bash
cd pedri-vs-bellingham
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
```

### 4. Activate the environment

For macOS/Linux:

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The dashboard should open automatically in your browser.

## 🧪 Testing

The repository includes test scripts for checking data loading and calculation logic.

Run the relevant test scripts from the project root:

```bash
python test_calculations.py
python test_data.py
```

Additional API and calculation test scripts are also included in the repository.

## 🔮 Future Improvements

Potential areas for further development include:

- Integrating verified football statistics from external data providers.
- Expanding the dataset with more complete competition-level statistics.
- Introducing additional performance metrics.
- Comparing players across different positions.
- Incorporating machine learning for player performance analysis.
- Developing player performance trends and predictive insights.

## 🎯 Project Objective

This project demonstrates the practical application of Python, data analysis, and interactive visualization in football analytics.

It combines data preparation, statistical calculations, and visual storytelling to turn football statistics into an interactive analytical experience.

## 👨‍💻 Author

**Ikemsinachi Okoroafor**

- GitHub: [@SINACHI01](https://github.com/SINACHI01)
- LinkedIn: [linkedin.com/in/sinachi12](https://www.linkedin.com/in/sinachi12/)

---

If you find this project interesting, feel free to explore the dashboard, star the repository, or contribute ideas for future improvements.

**Built with Python. Inspired by football. Driven by data.** ⚽📊
