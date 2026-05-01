from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    company: Mapped[str | None] = mapped_column(String(120), nullable=True)
    source_type: Mapped[str] = mapped_column(String(20), default="text")
    raw_text: Mapped[str] = mapped_column(Text)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sessions: Mapped[list["AssessmentSession"]] = relationship(back_populates="job_description")


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_name: Mapped[str] = mapped_column(String(160))
    headline: Mapped[str | None] = mapped_column(String(240), nullable=True)
    source_type: Mapped[str] = mapped_column(String(20), default="text")
    raw_text: Mapped[str] = mapped_column(Text)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sessions: Mapped[list["AssessmentSession"]] = relationship(back_populates="resume")


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(220))
    status: Mapped[str] = mapped_column(String(50), default="analysis_ready")
    job_description_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id"))
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    skill_match_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    overall_assessment_score: Mapped[float] = mapped_column(Float, default=0.0)
    overall_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    summary: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job_description: Mapped[JobDescription] = relationship(back_populates="sessions")
    resume: Mapped[Resume] = relationship(back_populates="sessions")
    skill_assessments: Mapped[list["SkillAssessment"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    questions: Mapped[list["Question"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    learning_plan_items: Mapped[list["LearningPlanItem"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class SkillAssessment(Base):
    __tablename__ = "skill_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("assessment_sessions.id"))
    skill_name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(80))
    importance: Mapped[int] = mapped_column(Integer)
    required: Mapped[bool] = mapped_column(Boolean, default=True)
    claimed: Mapped[bool] = mapped_column(Boolean, default=False)
    resume_match_score: Mapped[float] = mapped_column(Float, default=0.0)
    assessment_score: Mapped[float] = mapped_column(Float, default=0.0)
    final_skill_score: Mapped[float] = mapped_column(Float, default=0.0)
    gap_priority: Mapped[str] = mapped_column(String(20), default="Low")
    gap_priority_score: Mapped[float] = mapped_column(Float, default=0.0)
    explainability: Mapped[str] = mapped_column(Text, default="")
    evidence: Mapped[dict] = mapped_column(JSON, default=dict)

    session: Mapped[AssessmentSession] = relationship(back_populates="skill_assessments")
    questions: Mapped[list["Question"]] = relationship(
        back_populates="skill_assessment", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("assessment_sessions.id"))
    skill_assessment_id: Mapped[int] = mapped_column(ForeignKey("skill_assessments.id"))
    prompt: Mapped[str] = mapped_column(Text)
    guidance: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[str] = mapped_column(String(40), default="Intermediate")
    order_index: Mapped[int] = mapped_column(Integer)
    asked: Mapped[bool] = mapped_column(Boolean, default=False)
    answered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped[AssessmentSession] = relationship(back_populates="questions")
    skill_assessment: Mapped[SkillAssessment] = relationship(back_populates="questions")
    answer: Mapped["Answer | None"] = relationship(
        back_populates="question", cascade="all, delete-orphan", uselist=False
    )


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), unique=True)
    response_text: Mapped[str] = mapped_column(Text)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    feedback: Mapped[str] = mapped_column(Text, default="")
    explainability: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    question: Mapped[Question] = relationship(back_populates="answer")


class LearningPlanItem(Base):
    __tablename__ = "learning_plan_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("assessment_sessions.id"))
    skill_name: Mapped[str] = mapped_column(String(120))
    priority: Mapped[str] = mapped_column(String(20))
    focus_area: Mapped[str] = mapped_column(Text)
    estimated_hours: Mapped[int] = mapped_column(Integer)
    timeline: Mapped[str] = mapped_column(String(80))
    reason: Mapped[str] = mapped_column(Text)
    resources: Mapped[list] = mapped_column(JSON, default=list)

    session: Mapped[AssessmentSession] = relationship(back_populates="learning_plan_items")
