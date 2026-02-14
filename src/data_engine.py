import pandas as pd

class FIFAEngine:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self._preprocess()

    def _preprocess(self):
        # Handle messy currency strings (e.g., €150M -> 150000000)
        for col in ['value_eur', 'wage_eur']:
            if col in self.df.columns:
                self.df[col] = self.df[col].replace(r'[€KBM]', '', regex=True).astype(float)
        
        # Add Growth Metric
        self.df['potential_gap'] = self.df['potential'] - self.df['overall']

    def find_candidates(self, position, max_age=23, min_potential=80):
        """Finds top 3 young prospects based on potential."""
        query = self.df[
            (self.df['player_positions'].str.contains(position, case=False)) & 
            (self.df['age'] <= max_age) & 
            (self.df['potential'] >= min_potential)
        ]
        return query.sort_values(by='potential_gap', ascending=False).head(3)

    def get_team_stats(self, player_names):
        """Calculates the average stats of your current squad."""
        squad = self.df[self.df['short_name'].isin(player_names)]
        return squad[['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']].mean().to_dict()