from __future__ import annotations

from pathlib import Path

from app.readers.encoding_utils import read_text_with_fallback
from app.utils.logger import get_logger

logger = get_logger(__name__)


def read_txt_lines(path: str | Path) -> list[dict]:
    path = Path(path)
    text = read_text_with_fallback(path)
    lines: list[dict] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        lines.append(
            {
                "arquivo_origem": path.name,
                "pagina_origem": None,
                "linha_origem": line_number,
                "texto": line,
            }
        )

    logger.info("TXT lido: %s | linhas=%s", path.name, len(lines))
    return lines
