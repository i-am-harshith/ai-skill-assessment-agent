from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.skill_catalog import SKILL_CATALOG

HIGH_SIGNAL_MARKERS = ("must", "required", "need", "hands-on", "expert", "strong", "production")
MEDIUM_SIGNAL_MARKERS = ("experience", "build", "develop", "design", "own", "deliver")
LOW_SIGNAL_MARKERS = ("preferred", "nice to have", "bonus", "plus")
ACTION_VERBS = ("built", "designed", "implemented", "led", "owned", "optimized", "delivered", "launched")
YEARS_PATTERN = re.compile(r"\b\d+\+?\s*(?:years?|yrs?)\b")


@dataclass
class SkillSignal:
    name: str
    category: str
    evidence: list[str]
    occurrences: int
    importance: int
    score: float


def split_sentences(text: str) -> list[str]:
    raw_segments = re.split(r"(?<=[.!?\n])\s+", text)
    return [segment.strip() for segment in raw_segments if segment.strip()]


def _contains_term(sentence: str, term: str) -> bool:
    normalized = sentence.lower()
    return re.search(rf"(?<!\w){re.escape(term.lower())}(?!\w)", normalized) is not None


def _count_occurrences(text: str, term: str) -> int:
    return len(re.findall(rf"(?<!\w){re.escape(term.lower())}(?!\w)", text.lower()))


def _compute_job_importance(evidence: list[str], occurrences: int) -> int:
    score = 1 + min(2, max(0, occurrences - 1))
    combined = " ".join(evidence).lower()
    if any(marker in combined for marker in HIGH_SIGNAL_MARKERS):
        score += 2
    elif any(marker in combined for marker in MEDIUM_SIGNAL_MARKERS):
        score += 1
    if any(marker in combined for marker in LOW_SIGNAL_MARKERS):
        score = max(1, score - 1)
    return max(1, min(5, score))


def _compute_resume_strength(evidence: list[str], occurrences: int) -> int:
    combined = " ".join(evidence).lower()
    score = 40 + min(25, occurrences * 10)
    if any(verb in combined for verb in ACTION_VERBS):
        score += 20
    if YEARS_PATTERN.search(combined):
        score += 15
    if any(token in combined for token in ("scale", "latency", "performance", "revenue", "users", "%")):
        score += 10
    return max(35, min(100, score))


def extract_skill_signals(text: str, source_type: str) -> list[SkillSignal]:
    sentences = split_sentences(text)
    signals: list[SkillSignal] = []
    searchable_text = text.lower()

    for skill in SKILL_CATALOG:
        matched_sentences = [
            sentence for sentence in sentences if any(_contains_term(sentence, synonym) for synonym in skill.synonyms)
        ]
        if not matched_sentences:
            continue

        occurrences = sum(_count_occurrences(searchable_text, synonym) for synonym in skill.synonyms)
        evidence = matched_sentences[:3]

        if source_type == "job":
            importance = _compute_job_importance(evidence, occurrences)
            score = float(importance * 20)
        else:
            importance = 0
            score = float(_compute_resume_strength(evidence, occurrences))

        signals.append(
            SkillSignal(
                name=skill.name,
                category=skill.category,
                evidence=evidence,
                occurrences=occurrences,
                importance=importance,
                score=score,
            )
        )

    if source_type == "job":
        return sorted(signals, key=lambda item: (-item.importance, -item.occurrences, item.name))
    return sorted(signals, key=lambda item: (-item.score, -item.occurrences, item.name))
