from __future__ import annotations

from itertools import combinations

import pandas as pd

from app.config import DEFAULT_SUM_TOLERANCE, MAX_CANDIDATES_FOR_SUM, MAX_COMBINATION_SIZE
from app.models.enums import MatchType
from app.reconciliation.scoring import score_histories


def sum_match(
    source_row: pd.Series,
    candidate_pool: pd.DataFrame,
    tolerance: float = DEFAULT_SUM_TOLERANCE,
) -> tuple[list[str] | None, dict | None]:
    if candidate_pool.empty:
        return None, None

    source_value = round(float(source_row["valor_base"] or 0), 2)
    source_key = source_row.get("historico_chave") or ""

    candidates = candidate_pool.copy()
    candidates["distance"] = (candidates["valor_base"].fillna(0) - source_value).abs()
    candidates["score_hist"] = candidates["historico_chave"].map(
        lambda candidate_key: score_histories(source_key, candidate_key)
    )
    candidates = candidates.sort_values(by=["score_hist", "distance"], ascending=[False, True])
    candidates = candidates.head(MAX_CANDIDATES_FOR_SUM)

    rows = list(candidates.to_dict("records"))

    for size in range(2, MAX_COMBINATION_SIZE + 1):
        for combo in combinations(rows, size):
            combo_value = round(sum(float(row["valor_base"] or 0) for row in combo), 2)
            if abs(combo_value - source_value) <= tolerance:
                avg_score = round(
                    sum(float(row["score_hist"]) for row in combo) / len(combo), 2
                )
                combo_ids = [row["transaction_id"] for row in combo]
                return combo_ids, {
                    "match_type": MatchType.SOMA.value,
                    "score": avg_score,
                    "matched_value": combo_value,
                    "justification": f"Valor encontrado por soma de {len(combo_ids)} lançamentos.",
                }

    return None, None
