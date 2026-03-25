from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.utils.logger import get_logger

logger = get_logger(__name__)


def read_excel_file(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    engine = "openpyxl" if path.suffix.lower() == ".xlsx" else "xlrd"
    excel = pd.ExcelFile(path, engine=engine)
    frames: list[pd.DataFrame] = []

    for sheet_name in excel.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet_name, engine=engine)
        if df.empty:
            continue
        df["arquivo_origem"] = path.name
        df["aba_origem"] = sheet_name
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    merged = pd.concat(frames, ignore_index=True)
    logger.info(
        "Excel lido: %s | abas=%s | linhas=%s",
        path.name,
        len(frames),
        len(merged),
    )
    return merged
