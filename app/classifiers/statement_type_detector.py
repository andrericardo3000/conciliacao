from __future__ import annotations

import pandas as pd

from app.models.enums import StatementType


def detect_statement_type(df: pd.DataFrame) -> str:
    if df.empty:
        return StatementType.DESCONHECIDO.value

    has_debito = "debito" in df.columns and df["debito"].fillna(0).abs().sum() > 0
    has_credito = "credito" in df.columns and df["credito"].fillna(0).abs().sum() > 0
    has_valor = "valor_base" in df.columns and df["valor_base"].notna().any()

    if has_debito or has_credito:
        return StatementType.RAZAO.value

    if has_valor:
        return StatementType.GENERICO.value

    return StatementType.DESCONHECIDO.value
