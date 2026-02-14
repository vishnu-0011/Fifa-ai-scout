import ollama

class ScoutAgent:
    def __init__(self, model_name="qwen3:4b"):
        self.model = model_name

    def generate_report(self, candidate_data, team_weakness, team_stats):
        prompt = f"""
        [CONTEXT]
        My Team average Pace: {team_stats.get('pace', 'N/A')}, Defending: {team_stats.get('defending', 'N/A')}.
        Weakness identified: {team_weakness}

        [CANDIDATE]
        Name: {candidate_data['short_name']} | Age: {candidate_data['age']}
        Current: {candidate_data['overall']} | Potential: {candidate_data['potential']}
        Key Stats: Pace({candidate_data['pace']}), Phys({candidate_data['physic']}), Def({candidate_data['defending']})

        [TASK]
        As a Tactical Scout, explain how this player's development curve and stats 
        will specifically solve our 'Team Weakness'. Provide a 'Match Impact' score out of 10.
        """
        
        response = ollama.chat(model=self.model, messages=[
            {'role': 'system', 'content': 'You are a FIFA Technical Director specializing in Gap Analysis.'},
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']