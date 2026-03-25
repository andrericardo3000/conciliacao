from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.utils.helpers import ensure_parent


def export_results_to_excel(results: dict[str, pd.DataFrame], output_path: str | Path) -> Path:
    output_path = ensure_parent(output_path)

    sheet_map = {
        "BASE_NORMALIZADA": results.get("base_normalizada", pd.DataFrame()),
        "CONCILIADOS_EXATOS": results.get("conciliados_exatos", pd.DataFrame()),
        "CONCILIADOS_PROVAVEIS": results.get("conciliados_provaveis", pd.DataFrame()),
        "CONCILIADOS_POR_SOMA": results.get("conciliados_por_soma", pd.DataFrame()),
        "CREDITOS_NAO_ENCONTRADOS": results.get("creditos_nao_encontrados", pd.DataFrame()),
        "DEBITOS_EM_ABERTO": results.get("debitos_em_aberto", pd.DataFrame()),
        "REVISAO_MANUAL": results.get("revisao_manual", pd.DataFrame()),
        "RESUMO": results.get("resumo", pd.DataFrame()),
    }

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, frame in sheet_map.items():
            if frame is None or frame.empty:
                pd.DataFrame({"info": ["sem dados"]}).to_excel(
                    writer, sheet_name=sheet_name, index=False
                )
            else:
                frame.to_excel(writer, sheet_name=sheet_name, index=False)

    return Path(output_path)
