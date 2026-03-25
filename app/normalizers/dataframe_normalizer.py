from __future__ import annotations

import pandas as pd

from app.normalizers.column_mapper import map_columns
from app.normalizers.date_normalizer import normalize_date
from app.normalizers.text_normalizer import build_history_key, normalize_history
from app.normalizers.value_normalizer import parse_value


EXPECTED_OPTIONAL_COLUMNS = [
    "data",
    "historico",
    "valor",
    "debito",
    "credito",
    "saldo",
    "documento",
    "conta",
    "arquivo_origem",
    "aba_origem",
    "pagina_origem",
    "linha_origem",
    "texto_original",
]


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = map_columns(df).copy()

    for column in EXPECTED_OPTIONAL_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df["historico"] = df["historico"].fillna("").astype(str)
    df["historico_normalizado"] = df["historico"].map(normalize_history)
    df["historico_chave"] = df["historico"].map(build_history_key)

    df["data"] = df["data"].map(normalize_date)
    df["valor"] = df["valor"].map(parse_value)
    df["debito"] = df["debito"].map(parse_value)
    df["credito"] = df["credito"].map(parse_value)
    df["saldo"] = df["saldo"].map(parse_value)

    df["valor_base"] = df["valor"]
    mask_valor_base_missing = df["valor_base"].isna()
    df.loc[mask_valor_base_missing, "valor_base"] = (
        df.loc[mask_valor_base_missing, "debito"]
        .fillna(df.loc[mask_valor_base_missing, "credito"])
    )

    df["lado"] = "INDEFINIDO"
    df.loc[df["debito"].fillna(0) > 0, "lado"] = "DEBITO"
    df.loc[df["credito"].fillna(0) > 0, "lado"] = "CREDITO"
    df.loc[
        (df["lado"] == "INDEFINIDO") & df["valor_base"].notna(),
        "lado",
    ] = "GENERICO"

    df = df.reset_index(drop=True)
    df["transaction_id"] = [f"TX{i:06d}" for i in range(1, len(df) + 1)]

    ordered_columns = [
        "transaction_id",
        "arquivo_origem",
        "aba_origem",
        "pagina_origem",
        "linha_origem",
        "data",
        "historico",
        "historico_normalizado",
        "historico_chave",
        "valor",
        "debito",
        "credito",
        "saldo",
        "valor_base",
        "lado",
        "documento",
        "conta",
        "texto_original",
    ]

    return df[ordered_columns]
