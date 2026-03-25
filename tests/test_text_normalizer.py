from app.normalizers.text_normalizer import build_history_key, normalize_history


def test_normalize_history():
    value = normalize_history("Pgto ref. adto fornecedor Disktrans Comercial Ltda")
    assert value == "PGTO REF ADTO FORNECEDOR DISKTRANS COMERCIAL LTDA"


def test_build_history_key():
    value = build_history_key("Baixa adto fornecedor ref. tit: 526719 Disktrans Comercial Ltda")
    assert "DISKTRANS" in value
