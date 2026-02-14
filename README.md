# FIFA AI Scout

FIFA AI Scout is an interactive Streamlit application backed by an Ollama-powered assistant that helps analysts compare transfer targets against their current squad context. The workflow ingests FIFA player data, normalizes the schema, and feeds curated player snapshots to the `ScoutAgent`, which returns natural-language scouting briefs.

## Tech Stack

- Python 3.10+
- Streamlit for the UI layer
- Pandas for data engineering
- Ollama (running `qwen3:4b` by default) for tactical write-ups

## Dataset

Player data comes from the [FIFA Player Performance and Market Value Analytics](https://www.kaggle.com/datasets/jayjoshi37/fifa-player-performance-and-market-value-analytics/code) dataset on Kaggle. Drop the CSV into `data/raw/fifa_player_performance_market_value.csv`; the engine auto-detects column aliases (e.g., `overall_rating`, `player_name`) and synthesizes missing metric columns so different FIFA exports work out of the box.

## Features

- Player picker with cached dataset loading for snappy UX
- Optional squad baseline selector that averages chosen teammates to highlight gaps
- `ScoutAgent` prompt engineering that drives consistent tactical verdicts plus match-impact scoring
- Normalized currency and rating fields, plus computed `potential_gap` metric for upside sorting

## Project Structure

- `main.py` – Streamlit surface that wires the engine and agent together
- `src/data_engine.py` – Data ingestion, cleansing, caching, and `PlayerSnapshot` creation
- `src/scout_agent.py` – Ollama client + structured prompt builder
- `src/utils.py` – Reserved for shared helpers (currently empty)
- `data/` – Raw (tracked) and processed (gitignored) datasets
- `models/` – Space for exported weights or checkpoints (gitignored)
- `notebook/` – Exploratory notebooks

## Setup

1. Clone the repository and move into it.
2. Create a virtual environment (examples: `python -m venv .venv` or `py -3 -m venv fifa`).
3. Activate the env and install dependencies: `pip install -r requirements.txt`.
4. Install Ollama locally and pull the default model: `ollama pull qwen3:4b`.
5. Download the Kaggle CSV and place it at `data/raw/fifa_player_performance_market_value.csv`.

## Running the App

```bash
streamlit run main.py
```

The first run caches the `FIFAEngine` and the `ScoutAgent`. Use the sidebar to describe your team weakness and optionally select current-squad players to build the baseline. Press **Generate Scouting Report** to trigger the agent call.

## Troubleshooting

- **Missing columns**: Ensure the CSV headers match the Kaggle export. The engine auto-maps common aliases, but `overall_rating` (or `overall`) must exist.
- **Ollama import error**: Install the Python client with `pip install ollama` and confirm the Ollama daemon is running.
- **Streamlit cannot start**: Verify the virtual environment is activated when installing dependencies and launching the app.

## License

This project is intended for educational and research purposes only.
