from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Dict, Sequence, Tuple

import pandas as pd


_TEAM_METRIC_COLUMNS: Sequence[str] = (
    'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic'
)

_COLUMN_ALIASES = {
    'short_name': ('short_name', 'player_name', 'name'),
    'player_positions': ('player_positions', 'position', 'best_position'),
    'overall': ('overall', 'overall_rating', 'overall_score'),
    'potential': ('potential', 'potential_rating'),
    'value_eur': ('value_eur', 'market_value_eur'),
    'wage_eur': ('wage_eur', 'salary_eur'),
}

_METRIC_FILLERS: Dict[str, Callable[[pd.DataFrame], pd.Series]] = {
    'pace': lambda df: df['overall'],
    'shooting': lambda df: df['overall'],
    'passing': lambda df: df['overall'],
    'dribbling': lambda df: df['overall'],
    'defending': lambda df: df['overall'],
    'physic': lambda df: df['overall'],
}


@dataclass(frozen=True)
class PlayerSnapshot:
    """Lightweight immutable view over the fields the UI/agent needs."""

    short_name: str
    player_positions: str
    age: int
    overall: int
    potential: int
    pace: float
    physic: float
    defending: float
    potential_gap: float


class FIFAEngine:
    def __init__(self, csv_path: str) -> None:
        self.csv_path = csv_path
        self.df = self._preprocess(pd.read_csv(csv_path, low_memory=False))
        self._player_names = tuple(sorted(self.df['short_name'].dropna().unique()))

    @staticmethod
    @staticmethod
    def _currency_to_float(value) -> float:
        if pd.isna(value):
            return float('nan')

        normalized = str(value).strip().replace('€', '').upper()
        multiplier = 1.0
        if normalized.endswith('M'):
            multiplier = 1_000_000
            normalized = normalized[:-1]
        elif normalized.endswith('K'):
            multiplier = 1_000
            normalized = normalized[:-1]

        try:
            return float(normalized) * multiplier
        except ValueError:
            return float('nan')

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = self._apply_column_aliases(df)

        # Normalize currency fields so downstream math stays numeric.
        for col in ('value_eur', 'wage_eur'):
            if col in df.columns:
                df[col] = df[col].apply(self._currency_to_float)

        if 'potential' not in df.columns and 'overall' in df.columns:
            df['potential'] = df['overall']

        for col in ('overall', 'potential'):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        if 'overall' in df.columns:
            overall_median = df['overall'].median() if df['overall'].notna().any() else 0
            df['overall'] = df['overall'].fillna(overall_median)

        if 'potential' in df.columns:
            df['potential'] = df['potential'].fillna(df['overall'])

        for metric, filler in _METRIC_FILLERS.items():
            if metric not in df.columns:
                df[metric] = filler(df)
            else:
                df[metric] = pd.to_numeric(df[metric], errors='coerce').fillna(df['overall'])

        if 'player_positions' not in df.columns:
            df['player_positions'] = ''
        df['player_positions'] = df['player_positions'].fillna('')
        if df['player_positions'].dtype != object:
            df['player_positions'] = df['player_positions'].astype(str)

        df['short_name'] = df['short_name'].astype(str).str.strip()
        df['potential_gap'] = df['potential'] - df['overall']
        return df

    def _apply_column_aliases(self, df: pd.DataFrame) -> pd.DataFrame:
        rename_map = {}
        for canonical, aliases in _COLUMN_ALIASES.items():
            if canonical in df.columns:
                continue
            for alias in aliases:
                if alias in df.columns:
                    rename_map[alias] = canonical
                    break

        if rename_map:
            df = df.rename(columns=rename_map)

        if 'value_eur' not in df.columns and 'market_value_million_eur' in df.columns:
            df['value_eur'] = pd.to_numeric(
                df['market_value_million_eur'], errors='coerce'
            ) * 1_000_000

        if 'short_name' not in df.columns:
            if 'player_name' in df.columns:
                df['short_name'] = df['player_name']
            else:
                df['short_name'] = df.index.astype(str)

        if 'overall' not in df.columns:
            raise KeyError("Dataset does not contain an overall or overall_rating column.")

        return df

    def list_player_names(self) -> Sequence[str]:
        return self._player_names

    def get_player_snapshot(self, player_name: str) -> PlayerSnapshot:
        row = self.df[self.df['short_name'] == player_name]
        if row.empty:
            raise ValueError(f"Player '{player_name}' not found in dataset")
        record = row.iloc[0]
        return PlayerSnapshot(
            short_name=record['short_name'],
            player_positions=record['player_positions'],
            age=int(record['age']),
            overall=int(record['overall']),
            potential=int(record['potential']),
            pace=float(record['pace']),
            physic=float(record['physic']),
            defending=float(record['defending']),
            potential_gap=float(record['potential_gap'])
        )

    def find_candidates(self, position: str, max_age: int = 23, min_potential: int = 80) -> pd.DataFrame:
        """Find the highest-upside prospects for a given role."""
        mask = (
            self.df['player_positions'].str.contains(position, case=False, regex=False) &
            (self.df['age'] <= max_age) &
            (self.df['potential'] >= min_potential)
        )
        return self.df.loc[mask].sort_values('potential_gap', ascending=False).head(3)

    def get_team_stats(self, player_names: Sequence[str]) -> Dict[str, float]:
        """Compute averaged squad metrics, caching repeated combos."""
        names_key: Tuple[str, ...] = tuple(sorted(player_names))
        return self._get_team_stats_cached(names_key)

    @lru_cache(maxsize=32)
    def _get_team_stats_cached(self, player_names: Tuple[str, ...]) -> Dict[str, float]:
        if not player_names:
            return {col: float(self.df[col].mean()) for col in _TEAM_METRIC_COLUMNS}

        squad = self.df[self.df['short_name'].isin(player_names)]
        return {
            col: float(squad[col].mean()) if col in squad else float('nan')
            for col in _TEAM_METRIC_COLUMNS
        }