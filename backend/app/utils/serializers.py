from __future__ import annotations

from app.models.entities import Answer, AssessmentSession, JobDescription, LearningPlanItem, Question, Resume, SkillAssessment


def serialize_job_description(record: JobDescription) -> dict:
    return {
        "id": record.id,
        "title": record.title,
        "company": record.company,
        "source_type": record.source_type,
        "file_name": record.file_name,
        "created_at": record.created_at.isoformat(),
        "raw_text": record.raw_text,
        "preview": record.raw_text[:280],
    }


def serialize_resume(record: Resume) -> dict:
    return {
        "id": record.id,
        "candidate_name": record.candidate_name,
        "headline": record.headline,
        "source_type": record.source_type,
        "file_name": record.file_name,
        "created_at": record.created_at.isoformat(),
        "raw_text": record.raw_text,
        "preview": record.raw_text[:280],
    }


def serialize_answer(record: Answer | None) -> dict | None:
    if not record:
        return None
    return {
        "id": record.id,
        "question_id": record.question_id,
        "response_text": record.response_text,
        "score": round(record.score, 1),
        "feedback": record.feedback,
        "explainability": record.explainability,
        "created_at": record.created_at.isoformat(),
    }


def serialize_question(record: Question | None) -> dict | None:
    if not record:
        return None
    return {
        "id": record.id,
        "skill_assessment_id": record.skill_assessment_id,
        "skill_name": record.skill_assessment.skill_name,
        "prompt": record.prompt,
        "guidance": record.guidance,
        "difficulty": record.difficulty,
        "order_index": record.order_index,
        "answered": record.answered,
        "answer": serialize_answer(record.answer),
    }


def serialize_skill_assessment(record: SkillAssessment) -> dict:
    return {
        "id": record.id,
        "skill_name": record.skill_name,
        "category": record.category,
        "importance": record.importance,
        "required": record.required,
        "claimed": record.claimed,
        "resume_match_score": round(record.resume_match_score, 1),
        "assessment_score": round(record.assessment_score, 1),
        "final_skill_score": round(record.final_skill_score, 1),
        "gap_priority": record.gap_priority,
        "gap_priority_score": round(record.gap_priority_score, 1),
        "explainability": record.explainability,
        "evidence": record.evidence,
    }


def serialize_learning_plan_item(record: LearningPlanItem) -> dict:
    return {
        "id": record.id,
        "skill_name": record.skill_name,
        "priority": record.priority,
        "focus_area": record.focus_area,
        "estimated_hours": record.estimated_hours,
        "timeline": record.timeline,
        "reason": record.reason,
        "resources": record.resources,
    }


def serialize_session_detail(record: AssessmentSession) -> dict:
    ordered_skills = sorted(record.skill_assessments, key=lambda item: (-item.importance, item.skill_name))
    ordered_questions = sorted(record.questions, key=lambda item: item.order_index)
    ordered_plan = sorted(record.learning_plan_items, key=lambda item: item.timeline)
    total_questions = len(ordered_questions)
    answered_questions = sum(1 for question in ordered_questions if question.answered)

    return {
        "id": record.id,
        "name": record.name,
        "status": record.status,
        "skill_match_percentage": round(record.skill_match_percentage, 1),
        "overall_assessment_score": round(record.overall_assessment_score, 1),
        "overall_readiness_score": round(record.overall_readiness_score, 1),
        "created_at": record.created_at.isoformat(),
        "updated_at": record.updated_at.isoformat(),
        "job_description": serialize_job_description(record.job_description),
        "resume": serialize_resume(record.resume),
        "summary": record.summary,
        "skills": [serialize_skill_assessment(skill) for skill in ordered_skills],
        "questions": [serialize_question(question) for question in ordered_questions],
        "learning_plan": [serialize_learning_plan_item(item) for item in ordered_plan],
        "progress": {
            "answered_questions": answered_questions,
            "total_questions": total_questions,
            "completion_percentage": round((answered_questions / total_questions) * 100, 1) if total_questions else 0,
        },
    }
