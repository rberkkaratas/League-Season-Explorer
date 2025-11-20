import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_points_over_time(team_match_clean: pd.DataFrame, team: str | None = None):
    df = team_match_clean.copy()
    df = df.sort_values(["team", "matchweek"])
    df["cum_points"] = df.groupby("team")["points"].cumsum()

    if team:
        df_team = df[df["team"] == team]
        plt.figure(figsize=(8, 5))
        sns.lineplot(data=df_team, x="matchweek", y="cum_points", marker="o")
        plt.title(f"Cumulative points – {team}")
    else:
        plt.figure(figsize=(10, 7))
        sns.lineplot(
            data=df,
            x="matchweek",
            y="cum_points",
            hue="team",
            legend=False,
            alpha=0.4,
        )
        plt.title("Cumulative points – all teams")

    plt.xlabel("Matchweek")
    plt.ylabel("Cumulative points")
    plt.tight_layout()
    plt.show()


def plot_goals_for_against(team_match_clean: pd.DataFrame):
    agg = (
        team_match_clean
        .groupby("team")
        .agg(GF=("GF", "sum"), GA=("GA", "sum"))
        .reset_index()
    )

    # Goals scored
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=agg.sort_values("GF", ascending=False),
        x="team",
        y="GF",
    )
    plt.xticks(rotation=90)
    plt.title("Total goals scored (GF)")
    plt.tight_layout()
    plt.show()

    # Goals conceded
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=agg.sort_values("GA", ascending=False),
        x="team",
        y="GA",
    )
    plt.xticks(rotation=90)
    plt.title("Total goals conceded (GA)")
    plt.tight_layout()
    plt.show()


def plot_xg_vs_points(team_match_clean: pd.DataFrame):
    agg = (
        team_match_clean
        .groupby("team")
        .agg(
            xG=("xG", "sum"),
            points=("points", "sum"),
        )
        .reset_index()
    )

    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=agg, x="xG", y="points")

    # Label each point with team name
    for _, row in agg.iterrows():
        plt.text(row["xG"], row["points"], row["team"], fontsize=8)

    plt.xlabel("Total xG (season)")
    plt.ylabel("Total points (season)")
    plt.title("xG vs points – team level")
    plt.tight_layout()
    plt.show()
