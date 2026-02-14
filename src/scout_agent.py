import math
from typing import Mapping, Union

import ollama

from src.data_engine import PlayerSnapshot


def _fmt_metric(value: Union[float, int, None]) -> str:
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return "N/A"
        return f"{float(value):.1f}"
    except (TypeError, ValueError):
        return "N/A"


class ScoutAgent:
    def __init__(self, model_name: str = "qwen3:4b", temperature: float = 0.1) -> None:
        self.model = model_name
        self.temperature = temperature

    def generate_report(
        self,
        candidate: PlayerSnapshot,
        team_weakness: str,
        team_stats: Mapping[str, float]
    ) -> str:
        pace = _fmt_metric(team_stats.get('pace'))
        defending = _fmt_metric(team_stats.get('defending'))
        prompt = (
            "[CONTEXT]\n"
            f"Team baseline pace {pace} | defending {defending}\n"
            f"Weakness: {team_weakness}\n\n"
            "[CANDIDATE]\n"
            f"{candidate.short_name}, age {candidate.age}, role {candidate.player_positions}\n"
            f"Overall {candidate.overall} → Potential {candidate.potential} (∆{candidate.potential_gap:.0f})\n"
            f"Key stats pace {candidate.pace}, phys {candidate.physic}, def {candidate.defending}\n\n"
            "[TASK]\n"
            "Act as a tactical scout. 1) Explain how the player fixes the weakness "
            "using concrete match scenarios. 2) Describe development focus areas. 3) "
            "Return a Match Impact score out of 10 along with a one-line verdict."
        )

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a FIFA Technical Director specializing in gap analysis and player fit.'
                },
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': self.temperature}
        )
        return response['message']['content']