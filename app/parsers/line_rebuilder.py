from __future__ import annotations

import re
from typing import Iterable

from app.config import NOISE_PATTERNS
from app.utils.helpers import clean_whitespace


DATE_RE = re.compile(r"^\d{2}[/-]\d{2}[/-]\d{2,4}\b")


def is_noise_line(text: str) -> bool:
    value = clean_whitespace(text).lower()
    if not value:
        return True
    return any(pattern in value for pattern in NOISE_PATTERNS)


def rebuild_broken_lines(raw_lines: Iterable[dict]) -> list[dict]:
    rebuilt: list[dict] = []
    current: dict | None = None

    for item in raw_lines:
        text = clean_whitespace(item.get("texto", ""))
        if is_noise_line(text):
            continue

        if DATE_RE.match(text):
            if current:
                rebuilt.append(current)
            current = {
                "arquivo_origem": item.get("arquivo_origem"),
                "pagina_origem": item.get("pagina_origem"),
                "linha_origem": item.get("linha_origem"),
                "texto": text,
            }
            continue

        if current:
            current["texto"] = clean_whitespace(f"{current['texto']} {text}")

    if current:
        rebuilt.append(current)

    return rebuilt
