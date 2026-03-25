from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class MatchResult:
    match_id: str
    match_type: str
    score: float
    source_id: str
    target_ids: List[str] = field(default_factory=list)
    source_value: float = 0.0
    matched_value: float = 0.0
    difference: float = 0.0
    justification: str = ""
