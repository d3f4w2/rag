from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RagState:
    question: str
    field_hits: list[dict[str, float]] = field(default_factory=list)
    text_hits: list[dict[str, float]] = field(default_factory=list)
    image_hits: list[dict[str, float]] = field(default_factory=list)
    ranked_cases: list[dict[str, float | str]] = field(default_factory=list)
    evidence: list[dict[str, str | float]] = field(default_factory=list)
    answer: str = ""
