import pandas as pd

from app.normalizers.column_mapper import map_columns


def test_map_columns():
    df = pd.DataFrame(
        {
            "Descrição": ["A"],
            "Valor Titulo": [100],
            "Data": ["01/01/2025"],
        }
    )
    mapped = map_columns(df)
    assert "historico" in mapped.columns
    assert "valor" in mapped.columns
    assert "data" in mapped.columns
