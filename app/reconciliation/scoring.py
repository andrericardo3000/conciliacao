from __future__ import annotations

from rapidfuzz import fuzz


def score_histories(source_key: str, target_key: str) -> float:
    source_key = source_key or ""
    target_key = target_key or ""

    if not source_key or not target_key:
        return 0.0

    token_ratio = float(fuzz.token_sort_ratio(source_key, target_key))
    partial_ratio = float(fuzz.partial_ratio(source_key, target_key))

    source_tokens = set(source_key.split())
    target_tokens = set(target_key.split())
    if not source_tokens or not target_tokens:
        overlap = 0.0
    else:
        overlap = 100.0 * (len(source_tokens & target_tokens) / len(source_tokens | target_tokens))

    return round((token_ratio * 0.45) + (partial_ratio * 0.35) + (overlap * 0.20), 2)
