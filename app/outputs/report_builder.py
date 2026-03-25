from __future__ import annotations

import pandas as pd


def build_summary_card(results: dict[str, pd.DataFrame]) -> dict:
    resumo = results.get("resumo", pd.DataFrame())
    if resumo.empty:
        return {}

    summary = dict(zip(resumo["indicador"], resumo["valor"]))
    return summary
