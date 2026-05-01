from __future__ import annotations

from collections.abc import Iterable

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.models.entities import Answer, AssessmentSession, JobDescription, LearningPlanItem, Question, Resume, SkillAssessment
from app.services.llm_service import get_llm_service
from app.services.skill_catalog import SKILL_LOOKUP
from app.services.skill_extractor import SkillSignal, extract_skill_signals
from app.utils.serializers import serialize_answer


def create_session_name(candidate_name: str, job_title: str, override: str | None = None) -> str:
    if override and override.strip():
        return override.strip()
    return f"{candidate_name} x {job_title} Assessment"


def list_catalog(db: Session) -> dict:
    jobs = db.scalars(select(JobDescription).order_by(JobDescription.created_at.desc())).all()
    resumes = db.scalars(select(Resume).order_by(Resume.created_at.desc())).all()
    sessions = db.scalars(
        select(AssessmentSession)
        .options(
            selectinload(AssessmentSession.job_description),
            selectinload(AssessmentSession.resume),
            selectinload(AssessmentSession.skill_assessments),
            selectinload(AssessmentSession.questions).selectinload(Question.answer),
            selectinload(AssessmentSession.learning_plan_items),
        )
        .order_by(AssessmentSession.created_at.desc())
    ).all()
    return {
        "job_descriptions": [serialize_job_like(job) for job in jobs],
        "resumes": [serialize_resume_like(resume) for resume in resumes],
        "sessions": [serialize_session_like(session) for session in sessions],
    }


def list_sessions(db: Session) -> list[dict]:
    sessions = db.scalars(
        select(AssessmentSession)
        .options(
            selectinload(AssessmentSession.job_description),
            selectinload(AssessmentSession.resume),
            selectinload(AssessmentSession.skill_assessments),
            selectinload(AssessmentSession.questions).selectinload(Question.answer),
            selectinload(AssessmentSession.learning_plan_items),
        )
        .order_by(AssessmentSession.created_at.desc())
    ).all()
    return [serialize_session_like(session) for session in sessions]


def serialize_job_like(job: JobDescription) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "source_type": job.source_type,
        "file_name": job.file_name,
        "created_at": job.created_at.isoformat(),
        "preview": job.raw_text[:280],
    }


def serialize_resume_like(resume: Resume) -> dict:
    return {
        "id": resume.id,
        "candidate_name": resume.candidate_name,
        "headline": resume.headline,
        "source_type": resume.source_type,
        "file_name": resume.file_name,
        "created_at": resume.created_at.isoformat(),
        "preview": resume.raw_text[:280],
    }


def serialize_session_like(session: AssessmentSession) -> dict:
    answered_questions = sum(1 for question in session.questions if question.answered)
    total_questions = len(session.questions)
    return {
        "id": session.id,
        "name": session.name,
        "status": session.status,
        "skill_match_percentage": round(session.skill_match_percentage, 1),
        "overall_assessment_score": round(session.overall_assessment_score, 1),
        "overall_readiness_score": round(session.overall_readiness_score, 1),
        "job_title": session.job_description.title,
        "candidate_name": session.resume.candidate_name,
        "created_at": session.created_at.isoformat(),
        "progress": {
            "answered_questions": answered_questions,
            "total_questions": total_questions,
            "completion_percentage": round((answered_questions / total_questions) * 100, 1) if total_questions else 0,
        },
    }


def get_session_or_404(db: Session, session_id: int) -> AssessmentSession:
    session = db.scalar(
        select(AssessmentSession)
        .where(AssessmentSession.id == session_id)
        .options(
            selectinload(AssessmentSession.job_description),
            selectinload(AssessmentSession.resume),
            selectinload(AssessmentSession.skill_assessments).selectinload(SkillAssessment.questions).selectinload(
                Question.answer
            ),
            selectinload(AssessmentSession.questions).selectinload(Question.answer),
            selectinload(AssessmentSession.learning_plan_items),
        )
    )
    if not session:
        raise HTTPException(status_code=404, detail="Assessment session not found.")
    return session


def _weighted_average(items: Iterable[SkillAssessment], attr: str) -> float:
    items = list(items)
    denominator = sum(item.importance for item in items) or 1
    numerator = sum(getattr(item, attr) * item.importance for item in items)
    return numerator / denominator


def _match_percentage(jd_skills: list[SkillSignal], resume_map: dict[str, SkillSignal]) -> float:
    if not jd_skills:
        return 0.0
    weight_total = sum(skill.importance for skill in jd_skills) or 1
    matched = sum(skill.importance for skill in jd_skills if skill.name in resume_map)
    return (matched / weight_total) * 100


def _build_explainability(jd_skill: SkillSignal, resume_signal: SkillSignal | None) -> str:
    if resume_signal:
        return (
            f"{jd_skill.skill_name if hasattr(jd_skill, 'skill_name') else jd_skill.name} is required with importance "
            f"{jd_skill.importance}/5. Resume evidence was found in {len(resume_signal.evidence)} snippet(s), "
            f"driving a resume match score of {resume_signal.score:.0f}/100."
        )
    return (
        f"{jd_skill.name} is required with importance {jd_skill.importance}/5, but the resume does not surface clear evidence. "
        "Initial score is driven down until assessment answers provide proof."
    )


def _compute_gap_priority(importance: int, final_skill_score: float) -> tuple[str, float]:
    priority_score = max(0.0, min(100.0, importance * 14 + (100 - final_skill_score) * 0.65))
    if priority_score >= 72:
        return "High", priority_score
    if priority_score >= 45:
        return "Medium", priority_score
    return "Low", priority_score


def _update_learning_plan(db: Session, session: AssessmentSession) -> None:
    db.execute(delete(LearningPlanItem).where(LearningPlanItem.session_id == session.id))
    sorted_gaps = sorted(
        [skill for skill in session.skill_assessments if skill.final_skill_score < 80],
        key=lambda item: (-item.gap_priority_score, item.final_skill_score),
    )

    for index, skill in enumerate(sorted_gaps[:6], start=1):
        definition = SKILL_LOOKUP.get(skill.skill_name)
        estimated_hours = max(4, int(round((100 - skill.final_skill_score) / 6 + skill.importance * 1.5)))
        focus_area = (
            "Build a small portfolio project and document the architectural decisions."
            if skill.assessment_score < 60
            else "Strengthen implementation depth with one targeted exercise and one production-style walkthrough."
        )
        reason = (
            f"{skill.skill_name} is a {skill.gap_priority.lower()}-priority gap because its weighted score is "
            f"{skill.final_skill_score:.1f}/100 while job importance is {skill.importance}/5."
        )
        item = LearningPlanItem(
            session_id=session.id,
            skill_name=skill.skill_name,
            priority=skill.gap_priority,
            focus_area=focus_area,
            estimated_hours=estimated_hours,
            timeline=f"Week {index}",
            reason=reason,
            resources=list(definition.resources if definition else []),
        )
        db.add(item)


def _recompute_session_metrics(db: Session, session: AssessmentSession) -> None:
    skills = session.skill_assessments
    total_importance = sum(skill.importance for skill in skills) or 1
    matched_importance = sum(skill.importance for skill in skills if skill.claimed)
    session.skill_match_percentage = round((matched_importance / total_importance) * 100 if skills else 0.0, 2)
    answered_skills = [skill for skill in skills if any(question.answer for question in skill.questions)]
    session.overall_assessment_score = round(
        _weighted_average(answered_skills, "assessment_score") if answered_skills else 0.0,
        2,
    )
    session.overall_readiness_score = round(
        session.skill_match_percentage * 0.4 + session.overall_assessment_score * 0.6,
        2,
    )

    matching_skills = [skill.skill_name for skill in skills if skill.claimed]
    missing_skills = [skill.skill_name for skill in skills if not skill.claimed]
    priority_gaps = [
        skill.skill_name
        for skill in sorted(skills, key=lambda item: (-item.gap_priority_score, item.final_skill_score))[:3]
    ]
    strongest_skills = [
        skill.skill_name for skill in sorted(skills, key=lambda item: (-item.final_skill_score, -item.importance))[:3]
    ]
    session.summary = {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "priority_gaps": priority_gaps,
        "strongest_skills": strongest_skills,
        "formula": "Final Skill Score = 40% Resume Match + 60% Assessment Score",
        "total_required_skills": len(skills),
        "matched_skill_count": len(matching_skills),
    }
    _update_learning_plan(db, session)


def create_or_refresh_analysis_session(
    db: Session,
    job_description_id: int,
    resume_id: int,
    session_name: str | None = None,
) -> AssessmentSession:
    job = db.get(JobDescription, job_description_id)
    resume = db.get(Resume, resume_id)
    if not job or not resume:
        raise HTTPException(status_code=404, detail="Job description or resume not found.")

    existing = db.scalar(
        select(AssessmentSession)
        .where(
            AssessmentSession.job_description_id == job_description_id,
            AssessmentSession.resume_id == resume_id,
        )
        .order_by(AssessmentSession.created_at.desc())
    )
    if existing:
        db.delete(existing)
        db.commit()

    jd_skills = extract_skill_signals(job.raw_text, source_type="job")
    resume_skills = extract_skill_signals(resume.raw_text, source_type="resume")
    resume_map = {skill.name: skill for skill in resume_skills}

    session = AssessmentSession(
        name=create_session_name(resume.candidate_name, job.title, session_name),
        status="analysis_ready",
        job_description_id=job.id,
        resume_id=resume.id,
        skill_match_percentage=_match_percentage(jd_skills, resume_map),
    )
    db.add(session)
    db.flush()

    for jd_skill in jd_skills:
        resume_signal = resume_map.get(jd_skill.name)
        resume_match_score = round(resume_signal.score if resume_signal else 0.0, 2)
        final_skill_score = round((resume_match_score * 0.4), 2)
        gap_priority, gap_priority_score = _compute_gap_priority(jd_skill.importance, final_skill_score)
        record = SkillAssessment(
            session_id=session.id,
            skill_name=jd_skill.name,
            category=jd_skill.category,
            importance=jd_skill.importance,
            required=True,
            claimed=resume_signal is not None,
            resume_match_score=resume_match_score,
            assessment_score=0.0,
            final_skill_score=final_skill_score,
            gap_priority=gap_priority,
            gap_priority_score=gap_priority_score,
            explainability=_build_explainability(jd_skill, resume_signal),
            evidence={
                "job_snippets": jd_skill.evidence,
                "resume_snippets": resume_signal.evidence if resume_signal else [],
            },
        )
        db.add(record)

    db.flush()
    session = get_session_or_404(db, session.id)
    _recompute_session_metrics(db, session)
    db.commit()
    return get_session_or_404(db, session.id)


def ensure_questions(db: Session, session: AssessmentSession) -> None:
    if session.questions:
        return

    llm = get_llm_service()
    ordered_skills = sorted(
        session.skill_assessments,
        key=lambda item: (not item.claimed, -item.importance, -item.resume_match_score, -item.gap_priority_score),
    )
    target_skills = ordered_skills[: settings.max_assessment_skills]
    order_index = 1

    for skill in target_skills:
        generated = llm.generate_questions(skill.skill_name, skill.category, skill.importance)
        for prompt in generated[: settings.questions_per_skill]:
            db.add(
                Question(
                    session_id=session.id,
                    skill_assessment_id=skill.id,
                    prompt=prompt.prompt,
                    guidance=prompt.guidance,
                    difficulty=prompt.difficulty,
                    order_index=order_index,
                )
            )
            order_index += 1

    session.status = "assessment_in_progress"
    db.commit()


def get_next_question(session: AssessmentSession) -> Question | None:
    ordered_questions = sorted(session.questions, key=lambda item: item.order_index)
    for question in ordered_questions:
        if not question.answered:
            return question
    return None


def submit_answer(db: Session, session: AssessmentSession, question_id: int, response_text: str) -> dict:
    question = next((item for item in session.questions if item.id == question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found in this session.")

    llm = get_llm_service()
    evaluation = llm.evaluate_answer(question.skill_assessment.skill_name, response_text)

    if question.answer:
        db.delete(question.answer)
        db.flush()

    answer = Answer(
        question_id=question.id,
        response_text=response_text.strip(),
        score=evaluation.score,
        feedback=evaluation.feedback,
        explainability=evaluation.explainability,
    )
    db.add(answer)
    question.answer = answer
    question.answered = True
    question.asked = True
    db.flush()

    scores = [q.answer.score for q in question.skill_assessment.questions if q.answer]
    assessment_score = round(sum(scores) / len(scores), 2) if scores else 0.0
    question.skill_assessment.assessment_score = assessment_score
    question.skill_assessment.final_skill_score = round(
        question.skill_assessment.resume_match_score * 0.4 + assessment_score * 0.6,
        2,
    )
    gap_priority, gap_priority_score = _compute_gap_priority(
        question.skill_assessment.importance,
        question.skill_assessment.final_skill_score,
    )
    question.skill_assessment.gap_priority = gap_priority
    question.skill_assessment.gap_priority_score = gap_priority_score
    question.skill_assessment.explainability = (
        f"{question.skill_assessment.skill_name} uses 40% resume evidence "
        f"({question.skill_assessment.resume_match_score:.1f}) and 60% answer quality "
        f"({assessment_score:.1f}) to reach {question.skill_assessment.final_skill_score:.1f}."
    )

    if all(item.answered for item in session.questions):
        session.status = "completed"

    _recompute_session_metrics(db, session)
    db.commit()
    db.refresh(answer)
    return serialize_answer(answer)
