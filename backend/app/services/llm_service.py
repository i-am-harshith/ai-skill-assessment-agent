from __future__ import annotations

import json
from dataclasses import dataclass

from app.core.config import settings
from app.services.skill_catalog import SKILL_LOOKUP


@dataclass
class GeneratedQuestion:
    prompt: str
    guidance: str
    difficulty: str


@dataclass
class EvaluationResult:
    score: float
    feedback: str
    explainability: str


class MockLLMService:
    question_templates = {
        "Python": "Walk through a Python project where you designed the core modules, validation rules, and test strategy. What trade-offs did you make?",
        "React": "Describe a React interface you built. How did you structure state, components, and performance-sensitive interactions?",
        "FastAPI": "Explain how you would design a FastAPI service for authenticated CRUD operations, validation, and observability.",
        "OpenAI API": "Describe how you would integrate an LLM feature into a production app. How would you handle prompts, schemas, failures, and cost control?",
        "RAG": "Explain how you would design a retrieval-augmented generation workflow from ingestion to grounded answers and evaluation.",
        "Docker": "Tell me how you containerised an application. What decisions did you make around images, environments, and local developer workflow?",
        "AWS": "Describe a cloud deployment you have worked on. Which AWS services were used and how did you reason about reliability and cost?",
        "SQL": "Describe a database problem you solved with SQL. What query patterns, indexes, or schema choices mattered?",
    }

    def generate_questions(self, skill_name: str, category: str, importance: int) -> list[GeneratedQuestion]:
        prompt = self.question_templates.get(
            skill_name,
            f"Describe a real project where you used {skill_name}. What problem were you solving, what choices did you make, and how did you measure success?",
        )
        difficulty = "Advanced" if importance >= 5 else "Intermediate" if importance >= 3 else "Foundational"
        guidance = "Look for project context, decision-making, concrete implementation details, and measurable outcomes."
        return [GeneratedQuestion(prompt=prompt, guidance=guidance, difficulty=difficulty)]

    def evaluate_answer(self, skill_name: str, answer: str) -> EvaluationResult:
        lowered = answer.lower()
        if any(phrase in lowered for phrase in ("i don't know", "no experience", "not familiar", "haven't used")):
            return EvaluationResult(
                score=15.0,
                feedback="The answer is transparent but does not show practical experience yet. Focus on one guided project before reassessing this skill.",
                explainability="Low score because the response explicitly indicates limited hands-on exposure.",
            )

        skill = SKILL_LOOKUP.get(skill_name)
        concept_hits = 0
        if skill:
            concept_hits = sum(1 for concept in skill.concepts if concept.lower() in lowered)

        words = len(answer.split())
        structure_hits = sum(1 for token in ("because", "trade-off", "tradeoff", "so that", "result", "impact") if token in lowered)
        evidence_hits = sum(
            1
            for token in ("i built", "i designed", "i implemented", "i led", "project", "%", "latency", "users", "team")
            if token in lowered
        )

        base_score = 10 if words >= 20 else 0
        if words >= 45:
            base_score += 15
        if words >= 80:
            base_score += 10

        depth_score = min(35, concept_hits * 9 + (10 if words >= 70 else 6 if words >= 40 else 0))
        evidence_score = min(35, evidence_hits * 7 + (8 if any(char.isdigit() for char in answer) else 0))
        clarity_score = min(20, structure_hits * 5 + (6 if words >= 35 else 0))
        score = float(max(15, min(100, base_score + depth_score + evidence_score + clarity_score)))

        if score >= 80:
            feedback = "Strong answer with clear implementation detail and enough evidence to trust the claimed skill level."
        elif score >= 60:
            feedback = "Solid answer, but it would be stronger with more technical depth, trade-offs, or measurable outcomes."
        else:
            feedback = "The answer shows partial understanding, but more detail is needed around implementation choices and results."

        explainability = (
            f"Score built from technical depth ({depth_score:.0f}), concrete evidence ({evidence_score:.0f}), "
            f"and clarity/structure ({clarity_score:.0f})."
        )
        return EvaluationResult(score=score, feedback=feedback, explainability=explainability)


class OpenAIBackedLLMService(MockLLMService):
    def __init__(self) -> None:
        self.available = False
        self.client = None
        if not settings.enable_openai or not settings.openai_api_key:
            return
        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=settings.openai_api_key)
            self.available = True
        except Exception:
            self.available = False

    def generate_questions(self, skill_name: str, category: str, importance: int) -> list[GeneratedQuestion]:
        if not self.available or not self.client:
            return super().generate_questions(skill_name, category, importance)

        prompt = (
            "Return JSON with keys prompt, guidance, difficulty. "
            f"Create one assessment question for the skill {skill_name} in category {category} for importance {importance}."
        )
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You create concise, interview-style technical assessment questions in JSON."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )
            payload = json.loads(response.choices[0].message.content or "{}")
            return [
                GeneratedQuestion(
                    prompt=payload.get("prompt", super().generate_questions(skill_name, category, importance)[0].prompt),
                    guidance=payload.get(
                        "guidance",
                        "Look for project context, decision-making, concrete implementation details, and measurable outcomes.",
                    ),
                    difficulty=payload.get("difficulty", "Intermediate"),
                )
            ]
        except Exception:
            return super().generate_questions(skill_name, category, importance)

    def evaluate_answer(self, skill_name: str, answer: str) -> EvaluationResult:
        if not self.available or not self.client:
            return super().evaluate_answer(skill_name, answer)

        prompt = (
            "Return JSON with keys score, feedback, explainability. "
            f"Evaluate this answer for the skill {skill_name}: {answer}"
        )
        try:
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a strict technical interviewer scoring answers out of 100 in JSON."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )
            payload = json.loads(response.choices[0].message.content or "{}")
            return EvaluationResult(
                score=float(payload.get("score", 0)),
                feedback=payload.get("feedback", ""),
                explainability=payload.get("explainability", ""),
            )
        except Exception:
            return super().evaluate_answer(skill_name, answer)


def get_llm_service() -> MockLLMService | OpenAIBackedLLMService:
    if settings.enable_openai and settings.openai_api_key:
        return OpenAIBackedLLMService()
    return MockLLMService()
