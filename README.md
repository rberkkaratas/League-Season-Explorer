## Project 1 – League Season Explorer (FBref / Understat EDA)

**Goal:** Build a clean, reusable dataset and run exploratory data analysis (EDA) for a single league and season  
(e.g. **Serie A 2023–24**) using **FBref** (and optionally **Understat**) via `soccerdata`.

This project is inspired by the structure of Edd Webster’s `football_analytics` repo, in particular:

- `data/fbref/` and `data/understat/` folders for storing data :contentReference[oaicite:0]{index=0}  
- The “Aggregated Player/Team Performance data” and “Web Scraping Football Data” sections of the README :contentReference[oaicite:1]{index=1}  


---

### 1. Project Structure

Use a folder layout similar to `football_analytics` but simplified:

```text
league-season-explorer/
│
├── data/
│   ├── fbref/
│   │   ├── raw/          # raw CSVs from FBref via soccerdata
│   │   └── processed/    # cleaned, analysis-ready CSVs
│   ├── understat/
│   │   ├── raw/
│   │   └── processed/
│   └── interim/          # temporary merged data, joins, etc.
│
├── notebooks/
│   ├── 01_data_download.ipynb
│   └── 02_eda_league_season.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py         # league/season constants
│   ├── data_fetch.py     # functions to call soccerdata / ScraperFC
│   ├── data_cleaning.py  # standardisation of team names, dates, codes
│   └── plotting.py       # reusable plotting functions
│
├── environment.yml or requirements.txt
└── README.md             # (this file)
