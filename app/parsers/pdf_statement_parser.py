from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.parsers.generic_parser import parse_rebuilt_lines
from app.parsers.line_rebuilder import rebuild_broken_lines
from app.readers.pdf_reader import read_pdf_lines


def parse_pdf_statement(path: str | Path) -> pd.DataFrame:
    raw_lines = read_pdf_lines(path)
    rebuilt_lines = rebuild_broken_lines(raw_lines)
    return parse_rebuilt_lines(rebuilt_lines)
