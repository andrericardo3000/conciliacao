from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from app.normalizers.dataframe_normalizer import normalize_dataframe
from app.outputs.excel_exporter import export_results_to_excel
from app.parsers.pdf_statement_parser import parse_pdf_statement
from app.parsers.txt_statement_parser import parse_txt_statement
from app.readers.csv_reader import read_csv_file
from app.readers.excel_reader import read_excel_file
from app.reconciliation.engine import reconcile
from app.utils.logger import get_logger
from app.utils.validators import validate_input_files

logger = get_logger(__name__)


def _read_single_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return parse_pdf_statement(path)

    if suffix == ".txt":
        return parse_txt_statement(path)

    if suffix == ".csv":
        return read_csv_file(path)

    if suffix in {".xls", ".xlsx"}:
        return read_excel_file(path)

    raise ValueError(f"Extensão não suportada: {suffix}")


def process_files(input_paths: list[str], output_path: str) -> dict:
    validate_input_files(input_paths)

    raw_frames: list[pd.DataFrame] = []
    for file_path in input_paths:
        frame = _read_single_file(file_path)
        if frame is None or frame.empty:
            logger.warning("Arquivo sem dados aproveitáveis: %s", file_path)
            continue
        raw_frames.append(frame)

    if not raw_frames:
        raise RuntimeError("Nenhum dado válido foi encontrado nos arquivos informados.")

    combined = pd.concat(raw_frames, ignore_index=True)
    normalized = normalize_dataframe(combined)
    results = reconcile(normalized)
    export_results_to_excel(results, output_path)

    logger.info("Resultado exportado: %s", output_path)
    return results


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Conciliador Universal")
    parser.add_argument(
        "--input",
        nargs="+",
        required=True,
        help="Um ou mais arquivos de entrada.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do Excel final.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    process_files(input_paths=args.input, output_path=args.output)


if __name__ == "__main__":
    main()
