from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Transaction:
    transaction_id: str
    arquivo_origem: str
    aba_origem: Optional[str]
    pagina_origem: Optional[int]
    linha_origem: Optional[int]
    data: Optional[str]
    historico_original: str
    historico_normalizado: str
    historico_chave: str
    valor: Optional[float]
    debito: Optional[float]
    credito: Optional[float]
    saldo: Optional[float]
    lado: str
