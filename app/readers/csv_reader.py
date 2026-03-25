from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from app.utils.logger import get_logger

logger = get_logger(__name__)


def _detect_delimiter(sample: str) -> str:
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,\t,")
        return dialect.delimiter
    except csv.Error:
        return ";" if sample.count(";") >= sample.count(",") else ","


def read_csv_file(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]
    last_error = None

    for encoding in encodings:
        try:
            sample = path.read_text(encoding=encoding, errors="ignore")[:5000]
            delimiter = _detect_delimiter(sample)
            df = pd.read_csv(path, sep=delimiter, encoding=encoding)
            df["arquivo_origem"] = path.name
            df["aba_origem"] = None
            logger.info(
                "CSV lido: %s | linhas=%s | colunas=%s",
                path.name,
                len(df),
                len(df.columns),
            )
            return df
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    raise RuntimeError(f"Falha ao ler CSV {path.name}: {last_error}")
