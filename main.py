import math

import streamlit as st
from src.data_engine import FIFAEngine
from src.scout_agent import ScoutAgent

# Page Config
st.set_page_config(page_title="AI Tactical Scout", layout="wide")

@st.cache_resource
def load_systems():
    # Cache the engine and agent so they don't reload on every click
    engine = FIFAEngine('data/raw/fifa_player_performance_market_value.csv')
    scout = ScoutAgent(model_name="qwen3:4b")
    return engine, scout

engine, scout = load_systems()


def _prepare_stats_for_display(stats_dict):
    processed = {}
    for key, value in stats_dict.items():
        if value is None or (isinstance(value, float) and math.isnan(value)):
            processed[key] = None
        else:
            processed[key] = round(float(value), 1)
    return processed

st.title("⚽ FIFA AI Tactical Scout")
st.sidebar.header("Team Configuration")

# 1. Dynamic Player Selection
player_options = engine.list_player_names()
if not player_options:
    st.error("Dataset has no players to evaluate.")
    st.stop()

selected_player_name = st.selectbox(
    "Search & Select a Target Player:", player_options, index=0
)

# 2. Input Team Context
team_weakness = st.sidebar.text_area(
    "Define Team Gap/Weakness:", 
    "Our midfield lacks stamina and we concede goals late in the game."
)

# 2b. Baseline Squad Context
benchmark_players = st.sidebar.multiselect(
    "Current Squad (optional)", player_options, default=[],
    help="Select players from your roster to compare against the target."
)
team_stats = engine.get_team_stats(tuple(benchmark_players))
if not benchmark_players:
    st.sidebar.caption("Using overall dataset averages as the baseline.")

# 3. Dynamic Analysis Trigger
if st.button("Generate Scouting Report", use_container_width=True):
    try:
        candidate = engine.get_player_snapshot(selected_player_name)
    except ValueError as err:
        st.error(str(err))
        st.stop()

    with st.spinner(f"Qwen3:4b is analyzing {selected_player_name}..."):
        try:
            report = scout.generate_report(candidate, team_weakness, team_stats)
        except Exception as exc:  # pragma: no cover - defensive UI guard
            st.error(f"Model request failed: {exc}")
            st.stop()
    
    # UI Display
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Overall", candidate.overall, f"+{candidate.potential_gap:.0f} Potential")
        st.write(f"**Age:** {candidate.age}")
        st.write(f"**Position:** {candidate.player_positions}")
        
    with col2:
        st.subheader("Tactical Verdict")
        st.markdown(report)

    st.divider()
    st.subheader("Team Baseline Snapshot")
    st.json(_prepare_stats_for_display(team_stats))