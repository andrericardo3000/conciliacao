from __future__ import annotations

import pandas as pd

from app.classifiers.statement_type_detector import detect_statement_type
from app.reconciliation.credit_priority_rules import split_reason_entries
from app.reconciliation.exact_matcher import exact_match
from app.reconciliation.fuzzy_matcher import fuzzy_match
from app.reconciliation.sum_matcher import sum_match


def _build_match_record(
    source_row: pd.Series,
    target_ids: list[str],
    info: dict,
) -> dict:
    matched_value = info.get("matched_value", source_row.get("valor_base", 0.0))
    return {
        "match_id": None,
        "match_type": info["match_type"],
        "score": info["score"],
        "source_id": source_row["transaction_id"],
        "target_ids": ", ".join(target_ids),
        "source_value": source_row["valor_base"],
        "matched_value": matched_value,
        "difference": round(float(source_row["valor_base"] or 0) - float(matched_value or 0), 2),
        "source_history": source_row["historico"],
        "justification": info["justification"],
    }


def reconcile(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    statement_type = detect_statement_type(df)

    results = {
        "statement_type": statement_type,
        "base_normalizada": df.copy(),
        "conciliados_exatos": pd.DataFrame(),
        "conciliados_provaveis": pd.DataFrame(),
        "conciliados_por_soma": pd.DataFrame(),
        "creditos_nao_encontrados": pd.DataFrame(),
        "debitos_em_aberto": pd.DataFrame(),
        "revisao_manual": pd.DataFrame(),
        "resumo": pd.DataFrame(),
    }

    if df.empty:
        return results

    if statement_type != "RAZAO":
        genericos = df[df["lado"].isin(["GENERICO", "INDEFINIDO"])].copy()
        results["revisao_manual"] = genericos
        results["resumo"] = pd.DataFrame(
            [
                {"indicador": "tipo_base", "valor": statement_type},
                {"indicador": "linhas_lidas", "valor": len(df)},
                {"indicador": "revisao_manual", "valor": len(genericos)},
            ]
        )
        return results

    credits, debits = split_reason_entries(df)
    available_debits = debits.copy()
    matched_records_exact: list[dict] = []
    matched_records_fuzzy: list[dict] = []
    matched_records_sum: list[dict] = []
    not_found_credits: list[dict] = []

    for _, credit_row in credits.iterrows():
        exact_row, exact_info = exact_match(credit_row, available_debits)
        if exact_row is not None and exact_info is not None:
            matched_records_exact.append(
                _build_match_record(credit_row, [exact_row["transaction_id"]], exact_info)
            )
            available_debits = available_debits[
                available_debits["transaction_id"] != exact_row["transaction_id"]
            ]
            continue

        fuzzy_row, fuzzy_info = fuzzy_match(credit_row, available_debits)
        if fuzzy_row is not None and fuzzy_info is not None:
            matched_records_fuzzy.append(
                _build_match_record(credit_row, [fuzzy_row["transaction_id"]], fuzzy_info)
            )
            available_debits = available_debits[
                available_debits["transaction_id"] != fuzzy_row["transaction_id"]
            ]
            continue

        combo_ids, sum_info = sum_match(credit_row, available_debits)
        if combo_ids is not None and sum_info is not None:
            matched_records_sum.append(
                _build_match_record(credit_row, combo_ids, sum_info)
            )
            available_debits = available_debits[
                ~available_debits["transaction_id"].isin(combo_ids)
            ]
            continue

        not_found_credits.append(credit_row.to_dict())

    used_debits = set()
    for bucket in [matched_records_exact, matched_records_fuzzy, matched_records_sum]:
        for item in bucket:
            ids = [part.strip() for part in item["target_ids"].split(",") if part.strip()]
            used_debits.update(ids)

    debitos_em_aberto = debits[~debits["transaction_id"].isin(used_debits)].copy()

    def _add_match_ids(records: list[dict], prefix: str) -> pd.DataFrame:
        if not records:
            return pd.DataFrame()
        frame = pd.DataFrame(records)
        frame["match_id"] = [f"{prefix}{i:06d}" for i in range(1, len(frame) + 1)]
        columns = [
            "match_id",
            "match_type",
            "score",
            "source_id",
            "target_ids",
            "source_value",
            "matched_value",
            "difference",
            "source_history",
            "justification",
        ]
        return frame[columns]

    results["conciliados_exatos"] = _add_match_ids(matched_records_exact, "EX")
    results["conciliados_provaveis"] = _add_match_ids(matched_records_fuzzy, "PR")
    results["conciliados_por_soma"] = _add_match_ids(matched_records_sum, "SM")
    results["creditos_nao_encontrados"] = pd.DataFrame(not_found_credits)
    results["debitos_em_aberto"] = debitos_em_aberto

    results["resumo"] = pd.DataFrame(
        [
            {"indicador": "tipo_base", "valor": statement_type},
            {"indicador": "linhas_lidas", "valor": len(df)},
            {"indicador": "creditos_total", "valor": len(credits)},
            {"indicador": "debitos_total", "valor": len(debits)},
            {"indicador": "conciliados_exatos", "valor": len(results["conciliados_exatos"])},
            {"indicador": "conciliados_provaveis", "valor": len(results["conciliados_provaveis"])},
            {"indicador": "conciliados_por_soma", "valor": len(results["conciliados_por_soma"])},
            {"indicador": "creditos_nao_encontrados", "valor": len(results["creditos_nao_encontrados"])},
            {"indicador": "debitos_em_aberto", "valor": len(results["debitos_em_aberto"])},
        ]
    )

    return results
