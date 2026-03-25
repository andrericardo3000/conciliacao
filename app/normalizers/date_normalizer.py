from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import pandas as pd

from app.config import DATE_PATTERNS


def normalize_date(value: Any) -> Optional[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    text = str(value).strip()
    if not text:
        return None

    for pattern in DATE_PATTERNS:
        try:
            dt = datetime.strptime(text, pattern)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return text
