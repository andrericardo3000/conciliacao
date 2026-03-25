from __future__ import annotations

import pandas as pd


def split_reason_entries(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    credits = df[df["lado"] == "CREDITO"].copy()
    debits = df[df["lado"] == "DEBITO"].copy()
    return credits, debits
