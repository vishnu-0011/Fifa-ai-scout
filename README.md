# ⚽ FIFA AI Tactical Scout Agent

FIFA AI Tactical Scout is an **agentic** scouting system that goes beyond simple stat filtering. By leveraging **Qwen3:4b via Ollama**, it performs **Gap Analysis**—comparing a target player's growth trajectory and technical attributes against your team’s specific tactical weaknesses to produce a data-backed scouting verdict.

## 🚀 Key Features

- **Dynamic Player Search**: Instantly access and analyze any player from the FIFA dataset.
- **Gap Analysis Agent**: Describe your team weakness (e.g., “slow transition in midfield”), and the agent evaluates how a candidate specifically addresses that gap.
- **Growth Trajectory**: Computes the delta between current rating and potential to identify **high-velocity** prospects.
- **Local Inference**: Runs entirely on your machine (optimized for entry-level GPUs; tested on NVIDIA GTX 1650).

## 🛠️ Technical Stack

- **Brain**: Qwen3:4b (via Ollama)
- **Data Engine**: Pandas (preprocessing, currency conversion, growth metrics)
- **Frontend**: Streamlit
- **Backend**: Python

## 📊 Dataset

This project uses the Kaggle dataset: **FIFA Player Performance and Market Value Analytics**.

- Source: https://www.kaggle.com/datasets/jayjoshi37/fifa-player-performance-and-market-value-analytics
- Place the CSV at: `data/raw/fifa_player_performance_market_value.csv`

## 📂 Project Structure

```text
fifa-ai-scout/
├── data/
│   ├── raw/                # Kaggle FIFA Dataset
│   └── processed/          # Cached/processed outputs
├── src/
│   ├── data_engine.py      # Data cleaning & stat logic
│   ├── scout_agent.py      # LLM orchestration & prompts
│   └── utils.py            # Shared helpers
├── main.py                 # Streamlit UI & orchestration
├── requirements.txt        # Project dependencies
└── notebook/               # Exploration notebooks
```

## ⚙️ Installation & Setup

### 1) Clone the repo

```bash
git clone https://github.com/vishnu-0011/Fifa-ai-scout.git
cd Fifa-ai-scout
```

### 2) Set up a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows (PowerShell)**: `venv\Scripts\Activate.ps1`
- **Windows (cmd)**: `venv\Scripts\activate.bat`
- **macOS/Linux**: `source venv/bin/activate`

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 3) Pull the AI model

Ensure Ollama is installed and running, then:

```bash
ollama pull qwen3:4b
```

### 4) Add the dataset

Download the Kaggle CSV and place it here:

`data/raw/fifa_player_performance_market_value.csv`

## ▶️ Run the application

```bash
streamlit run main.py
```

## 🧠 Why Qwen3:4b?

This project is optimized for local performance on consumer hardware. **Qwen3:4b** provides strong reasoning for its size, enabling tactical scouting reports without overwhelming a **4GB VRAM** GPU like the GTX 1650.

## 🧩 Notes / Troubleshooting

- If you get Ollama connection errors, confirm the Ollama service is running and that `ollama run qwen3:4b` works in a terminal.
- If Streamlit fails to start, ensure your virtual environment is activated before running `streamlit run main.py`.

## License

This project is intended for educational and research purposes only.
