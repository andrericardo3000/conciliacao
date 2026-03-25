from __future__ import annotations

from enum import Enum


class StatementType(str, Enum):
    RAZAO = "RAZAO"
    GENERICO = "GENERICO"
    EXTRATO = "EXTRATO"
    DESCONHECIDO = "DESCONHECIDO"


class EntrySide(str, Enum):
    DEBITO = "DEBITO"
    CREDITO = "CREDITO"
    GENERICO = "GENERICO"
    INDEFINIDO = "INDEFINIDO"


class MatchType(str, Enum):
    EXATO = "EXATO"
    PROVAVEL = "PROVAVEL"
    SOMA = "SOMA"
