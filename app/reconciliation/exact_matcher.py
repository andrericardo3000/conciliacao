from __future__ import annotations

import pandas as pd

from app.models.enums import MatchType


def exact_match(source_row: pd.Series, candidate_pool: pd.DataFrame) -> tuple[pd.Series | None, dict | None]:
    if candidate_pool.empty:
        return None, None

    source_value = round(float(source_row["valor_base"] or 0), 2)
    source_key = (source_row.get("historico_chave") or "").strip()

    candidates = candidate_pool.copy()
    candidates = candidates[candidates["valor_base"].round(2) == source_value]

    if source_key:
        exact_key = candidates[candidates["historico_chave"] == source_key]
        if not exact_key.empty:
            chosen = exact_key.iloc[0]
            return chosen, {
                "match_type": MatchType.EXATO.value,
                "score": 100.0,
                "justification": "Valor igual e chave do histórico igual.",
            }

    exact_normalized = candidates[
        candidates["historico_normalizado"] == source_row.get("historico_normalizado")
    ]
    if not exact_normalized.empty:
        chosen = exact_normalized.iloc[0]
        return chosen, {
            "match_type": MatchType.EXATO.value,
            "score": 98.0,
            "justification": "Valor igual e histórico normalizado igual.",
        }

    return None, None
