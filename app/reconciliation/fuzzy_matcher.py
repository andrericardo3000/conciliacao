from __future__ import annotations

import pandas as pd

from app.config import DEFAULT_FUZZY_THRESHOLD
from app.models.enums import MatchType
from app.reconciliation.scoring import score_histories


def fuzzy_match(
    source_row: pd.Series,
    candidate_pool: pd.DataFrame,
    threshold: int = DEFAULT_FUZZY_THRESHOLD,
) -> tuple[pd.Series | None, dict | None]:
    if candidate_pool.empty:
        return None, None

    source_value = round(float(source_row["valor_base"] or 0), 2)
    source_key = source_row.get("historico_chave") or ""
    source_date = source_row.get("data")

    candidates = candidate_pool.copy()
    candidates = candidates[candidates["valor_base"].round(2) == source_value]
    if candidates.empty:
        return None, None

    candidates["score_hist"] = candidates["historico_chave"].map(
        lambda candidate_key: score_histories(source_key, candidate_key)
    )

    if source_date:
        candidates["date_bonus"] = (candidates["data"] == source_date).astype(float) * 3.0
    else:
        candidates["date_bonus"] = 0.0

    candidates["final_score"] = candidates["score_hist"] + candidates["date_bonus"]
    candidates = candidates.sort_values(by=["final_score"], ascending=False)

    best = candidates.iloc[0]
    if float(best["final_score"]) < threshold:
        return None, None

    return best, {
        "match_type": MatchType.PROVAVEL.value,
        "score": round(float(best["final_score"]), 2),
        "justification": "Valor igual e histórico semelhante acima do limite configurado.",
    }
