from pathlib import Path
import re

import numpy as np
import pandas as pd

from .config import FBREF_RAW_DIR, FBREF_PROCESSED_DIR


# ---------- Helper functions ---------- #
def extract_team_from_url(url: str):
    """
    From a FBref squad URL like:
      /en/squads/922493f3/2023-2024/Atalanta-Stats
    return 'Atalanta'.
    """
    if isinstance(url, str):
        m = re.search(r"/\d{4}-\d{4}/([^/]+)-Stats", url)
        if m:
            name = m.group(1)
            return name.replace("-", " ")
    return np.nan


def points_from_result(res: str):
    """
    Convert 'W'/'D'/'L' to 3/1/0.
    """
    if res == "W":
        return 3
    if res == "D":
        return 1
    if res == "L":
        return 0
    return np.nan


def parse_score(score: str):
    """
    Parse score string '2–1' (with en dash) into (home_goals, away_goals).
    """
    if pd.isna(score):
        return np.nan, np.nan

    s = str(score).replace("–", "-").replace("—", "-")
    try:
        home, away = s.split("-")
        return float(home), float(away)
    except Exception:
        return np.nan, np.nan


# ---------- Cleaning functions ---------- #

def clean_team_season_standard() -> pd.DataFrame:
    path = FBREF_RAW_DIR / "team_season_stats_standard.csv"
    df = pd.read_csv(path)

    # Create 'team' from url
    df["team"] = df["url"].apply(extract_team_from_url)

    # Drop meta row (where team is NaN)
    df_clean = df[df["team"].notna()].reset_index(drop=True)

    FBREF_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FBREF_PROCESSED_DIR / "team_season_clean.csv"
    df_clean.to_csv(out_path, index=False)
    print(f"Saved cleaned team season stats to {out_path}")
    return df_clean


def clean_team_match_standard(team_season_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Clean team_match_stats_standard.csv (stat_type='schedule'):
    - parse date
    - reconstruct 'team' column using team_season_clean order
    - derive 'matchweek' from 'round'
    - compute 'points'
    """
    path = FBREF_RAW_DIR / "team_match_stats_standard.csv"
    df = pd.read_csv(path)

    # Parse date
    df["date"] = pd.to_datetime(df["date"])

    # Rebuild team column:
    #  - number of teams = len(team_season_clean)
    #  - each team should have same number of rows (matches_per_team)
    teams = team_season_clean["team"].tolist()
    n_teams = len(teams)
    matches_per_team = len(df) // n_teams  # e.g. 760 / 20 = 38

    df["team"] = np.repeat(teams, matches_per_team)

    # Extract matchweek as integer from 'round' (e.g. 'Matchweek 5')
    if "round" in df.columns:
        df["matchweek"] = (
            df["round"]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype(int)
        )

    # Points per game
    df["points"] = df["result"].apply(points_from_result)

    FBREF_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FBREF_PROCESSED_DIR / "team_match_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned team match stats to {out_path}")
    return df


def clean_schedule() -> pd.DataFrame:
    """
    Clean schedule.csv:
    - parse dates
    - split 'score' into home_goals, away_goals
    """
    path = FBREF_RAW_DIR / "schedule.csv"
    df = pd.read_csv(path)

    # Parse date
    df["date"] = pd.to_datetime(df["date"])

    # Parse goals
    home_goals, away_goals = zip(*df["score"].map(parse_score))
    df["home_goals"] = home_goals
    df["away_goals"] = away_goals

    FBREF_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FBREF_PROCESSED_DIR / "schedule_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned schedule to {out_path}")
    return df
