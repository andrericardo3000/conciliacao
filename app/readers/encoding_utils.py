from __future__ import annotations

from pathlib import Path


def read_text_with_fallback(path: str | Path) -> str:
    path = Path(path)
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]

    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    return path.read_text(encoding="latin-1", errors="ignore")
