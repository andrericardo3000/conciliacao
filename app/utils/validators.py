from __future__ import annotations

from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".csv", ".xls", ".xlsx"}


def validate_input_files(file_paths: list[str]) -> None:
    if not file_paths:
        raise ValueError("Nenhum arquivo foi informado.")

    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Extensão não suportada: {path.suffix}. "
                f"Extensões válidas: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )
