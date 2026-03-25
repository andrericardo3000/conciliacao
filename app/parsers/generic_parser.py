from __future__ import annotations

import re
from typing import Optional

import pandas as pd

from app.config import PDF_TXT_CREDIT_HINTS, PDF_TXT_DEBIT_HINTS
from app.utils.helpers import clean_whitespace


DATE_RE = re.compile(r"^(?P<data>\d{2}[/-]\d{2}[/-]\d{2,4})\s+")
AMOUNT_RE = re.compile(r"(?<!\d)(?:\d{1,3}(?:\.\d{3})*|\d+),\d{2}(?!\d)")


def _to_float_br(value: str | None) -> Optional[float]:
    if value is None:
        return None
    value = str(value).strip().replace(".", "").replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


def infer_side_by_keywords(history: str) -> str:
    upper = clean_whitespace(history).upper()
    if any(token in upper for token in PDF_TXT_CREDIT_HINTS):
        return "CREDITO"
    if any(token in upper for token in PDF_TXT_DEBIT_HINTS):
        return "DEBITO"
    return "INDEFINIDO"


def parse_rebuilt_lines(lines: list[dict]) -> pd.DataFrame:
    records: list[dict] = []

    for item in lines:
        text = item["texto"]
        date_match = DATE_RE.match(text)
        if not date_match:
            continue

        data = date_match.group("data")
        remainder = text[date_match.end():].strip()

        amounts = AMOUNT_RE.findall(remainder)
        if not amounts:
            continue

        amount_values = [_to_float_br(value) for value in amounts]
        history_without_amounts = remainder
        for amount in amounts:
            history_without_amounts = history_without_amounts.replace(amount, " ", 1)
        history_without_amounts = clean_whitespace(history_without_amounts)

        debito = None
        credito = None
        saldo = None
        valor = None

        if len(amount_values) >= 3:
            debito, credito, saldo = amount_values[-3], amount_values[-2], amount_values[-1]
            valor = (debito or 0.0) if (debito or 0.0) > 0 else (credito or 0.0)
        elif len(amount_values) == 2:
            valor, saldo = amount_values[0], amount_values[1]
        else:
            valor = amount_values[0]

        inferred_side = infer_side_by_keywords(history_without_amounts)
        if valor and debito is None and credito is None:
            if inferred_side == "DEBITO":
                debito = valor
            elif inferred_side == "CREDITO":
                credito = valor

        records.append(
            {
                "arquivo_origem": item.get("arquivo_origem"),
                "aba_origem": None,
                "pagina_origem": item.get("pagina_origem"),
                "linha_origem": item.get("linha_origem"),
                "data": data,
                "historico": history_without_amounts,
                "valor": valor,
                "debito": debito,
                "credito": credito,
                "saldo": saldo,
                "texto_original": text,
            }
        )

    return pd.DataFrame.from_records(records)
