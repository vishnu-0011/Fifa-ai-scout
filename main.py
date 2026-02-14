from src.data_engine import FIFAEngine
from src.scout_agent import ScoutAgent

def run_scouting_mission():
    # 1. Setup
    engine = FIFAEngine('data/raw/players_22.csv') # Update path as needed
    scout = ScoutAgent()

    # 2. Define your current situation
    my_current_squad = ['L. Messi', 'K. De Bruyne'] # Example players in your team
    weakness = "We are losing matches in the second half because our midfield lacks recovery speed and stamina."

    # 3. Execution
    print("--- Searching for Young Talents to fix gaps ---")
    candidates = engine.find_candidates(position='CM', max_age=22)
    team_averages = engine.get_team_stats(my_current_squad)

    for _, player in candidates.iterrows():
        print(f"\nAnalyzing: {player['short_name']}...")
        report = scout.generate_report(player, weakness, team_averages)
        print(f"REPORT:\n{report}\n{'-'*50}")

if __name__ == "__main__":
    run_scouting_mission()