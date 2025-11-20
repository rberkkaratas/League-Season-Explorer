from pathlib import Path
import soccerdata as sd

from .config import LEAGUE_ID_FBREF, SEASON_FBREF, DATA_DIR


def get_fbref_client():
    fbref = sd.FBref(
        leagues=LEAGUE_ID_FBREF,
        seasons=SEASON_FBREF,
    )
    return fbref


def fetch_fbref_data():
    fbref = get_fbref_client()

    # 1. Match schedule (fixtures, results, goals/xG, etc.)
    schedule = fbref.read_schedule()

    # 2. Team season stats (overall summary per team)
    team_season_stats = fbref.read_team_season_stats(stat_type="standard")

    # 3. Team match stats (one row per team per match)
    #    IMPORTANT: we use stat_type="schedule" here.
    team_match_stats = fbref.read_team_match_stats(stat_type="schedule")

    raw_dir = Path(DATA_DIR) / "fbref" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    schedule.to_csv(raw_dir / "schedule.csv", index=False)
    team_season_stats.to_csv(raw_dir / "team_season_stats_standard.csv", index=False)
    team_match_stats.to_csv(raw_dir / "team_match_stats_standard.csv", index=False)

    print("Saved FBref raw data to:", raw_dir)