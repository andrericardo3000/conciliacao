from __future__ import annotations

import re

from app.config import TEXT_STOPWORDS_FOR_KEY
from app.utils.helpers import clean_whitespace, strip_accents


def normalize_history(text: str) -> str:
    value = strip_accents(str(text or "")).upper()
    value = re.sub(r"[\r\n\t]+", " ", value)
    value = re.sub(r"[^A-Z0-9/ ]+", " ", value)
    value = clean_whitespace(value)
    return value


def build_history_key(text: str) -> str:
    value = normalize_history(text)
    tokens = [
        token
        for token in value.split()
        if token not in TEXT_STOPWORDS_FOR_KEY and len(token) > 1
    ]
    return " ".join(tokens)
