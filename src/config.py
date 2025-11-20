from pathlib import Path

# League & season for FBref via soccerdata
LEAGUE_ID_FBREF = "ITA-Serie A"   # or whatever league
SEASON_FBREF = "2023-24"       

# Data directories
DATA_DIR = Path("../data")
FBREF_RAW_DIR = DATA_DIR / "fbref" / "raw"
FBREF_PROCESSED_DIR = DATA_DIR / "fbref" / "processed"
