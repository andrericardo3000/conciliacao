from __future__ import annotations

COLUMN_ALIASES = {
    "data": [
        "data",
        "dt",
        "data lancamento",
        "data lançamento",
        "data mov",
        "data movimento",
        "data lcto",
    ],
    "historico": [
        "historico",
        "histórico",
        "descricao",
        "descrição",
        "hist",
        "desc",
        "complemento",
        "detalhe",
        "texto",
    ],
    "valor": [
        "valor",
        "valor titulo",
        "valor título",
        "valor tit",
        "saldo",
        "saldo titulo",
        "saldo título",
        "saldo tit",
        "valor base",
        "vlr",
    ],
    "debito": ["debito", "débito", "vl debito", "vl débito"],
    "credito": ["credito", "crédito", "vl credito", "vl crédito"],
    "saldo": ["saldo final", "saldo acumulado", "saldo atual", "saldo"],
    "documento": ["documento", "doc", "titulo", "título", "numero", "número"],
    "conta": ["conta", "conta contabil", "conta contábil", "cod conta", "código conta"],
    "filial": ["filial", "empresa", "loja", "unidade"],
    "contrapartida": ["contrapartida", "contra partida", "contra-partida"],
}

NOISE_PATTERNS = [
    "razao",
    "razão",
    "valores expressos",
    "período:",
    "periodo:",
    "cnpj:",
    "pág:",
    "pag:",
    "página",
    "pagina",
    "conta:",
    "titulo:",
    "título:",
]

PDF_TXT_DEBIT_HINTS = [
    "PGTO",
    "PAGTO",
    "PAGAMENTO",
    "ADTO",
    "ADIANTAMENTO",
    "TRANSFERENCIA ENVIADA",
    "TARIFA",
    "DEBITO",
    "DÉBITO",
]

PDF_TXT_CREDIT_HINTS = [
    "BAIXA",
    "LIQUIDACAO",
    "LIQUIDAÇÃO",
    "ESTORNO",
    "CREDITO",
    "CRÉDITO",
    "RECEBIMENTO",
    "RECUPERACAO",
    "RECUPERAÇÃO",
]

TEXT_STOPWORDS_FOR_KEY = {
    "PGTO",
    "PAGTO",
    "PAGAMENTO",
    "REF",
    "REFERENTE",
    "BAIXA",
    "LIQUIDACAO",
    "LIQUIDAÇÃO",
    "ADTO",
    "ADIANTAMENTO",
    "FORNECEDOR",
    "CLIENTE",
    "TIT",
    "TITULO",
    "TÍTULO",
    "DOC",
    "DOCUMENTO",
    "NF",
    "NFE",
    "FILIAL",
    "LOJA",
    "CONFORME",
    "REGISTRO",
    "NA",
    "NO",
    "DE",
    "DA",
    "DO",
    "DAS",
    "DOS",
    "A",
    "O",
    "E",
}

DATE_PATTERNS = [
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d/%m/%y",
    "%d-%m-%y",
]

DEFAULT_FUZZY_THRESHOLD = 72
DEFAULT_SUM_TOLERANCE = 0.01
MAX_COMBINATION_SIZE = 3
MAX_CANDIDATES_FOR_SUM = 12
