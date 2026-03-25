from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from app.utils.logger import get_logger

logger = get_logger(__name__)


def read_pdf_lines(path: str | Path) -> list[dict]:
    path = Path(path)
    lines: list[dict] = []

    reader = PdfReader(str(path))
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line_number, line in enumerate(text.splitlines(), start=1):
            lines.append(
                {
                    "arquivo_origem": path.name,
                    "pagina_origem": page_number,
                    "linha_origem": line_number,
                    "texto": line,
                }
            )

    logger.info("PDF lido: %s | linhas=%s", path.name, len(lines))
    return lines
