from __future__ import annotations

import re

import pandas as pd

from app.config import COLUMN_ALIASES
from app.utils.helpers import clean_whitespace, strip_accents


def normalize_column_name(value: str) -> str:
    value = strip_accents(str(value or "")).lower()
    value = clean_whitespace(value)
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return clean_whitespace(value)


def map_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    rename_map: dict[str, str] = {}
    normalized_to_original = {
        normalize_column_name(column): column for column in df.columns
    }

    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            alias_normalized = normalize_column_name(alias)
            if alias_normalized in normalized_to_original:
                rename_map[normalized_to_original[alias_normalized]] = canonical
                break

    return df.rename(columns=rename_map)
