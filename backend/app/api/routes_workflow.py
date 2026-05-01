from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.requests import AnalyzeRequest, AnswerRequest
from app.services.assessment_engine import (
    create_or_refresh_analysis_session,
    ensure_questions,
    get_next_question,
    get_session_or_404,
    submit_answer,
)
from app.services.file_parser import resolve_text_payload
from app.services.seed import create_job_description_record, create_resume_record
from app.utils.serializers import (
    serialize_job_description,
    serialize_question,
    serialize_resume,
    serialize_session_detail,
)

router = APIRouter()


@router.post("/job-descriptions")
async def create_job_description(
    title: str = Form(...),
    company: str | None = Form(default=None),
    raw_text: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
) -> dict:
    content, source_type, file_name = await resolve_text_payload(file=file, raw_text=raw_text)
    record = create_job_description_record(
        db=db,
        title=title.strip(),
        company=(company or "").strip() or None,
        raw_text=content,
        source_type=source_type,
        file_name=file_name,
    )
    return serialize_job_description(record)


@router.post("/resumes")
async def create_resume(
    candidate_name: str = Form(...),
    headline: str | None = Form(default=None),
    raw_text: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
) -> dict:
    content, source_type, file_name = await resolve_text_payload(file=file, raw_text=raw_text)
    record = create_resume_record(
        db=db,
        candidate_name=candidate_name.strip(),
        headline=(headline or "").strip() or None,
        raw_text=content,
        source_type=source_type,
        file_name=file_name,
    )
    return serialize_resume(record)


@router.post("/sessions/analyze")
def analyze_candidate(request: AnalyzeRequest, db: Session = Depends(get_db)) -> dict:
    session = create_or_refresh_analysis_session(
        db=db,
        job_description_id=request.job_description_id,
        resume_id=request.resume_id,
        session_name=request.session_name,
    )
    return serialize_session_detail(session)


@router.post("/sessions/{session_id}/questions/generate")
def generate_questions(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = get_session_or_404(db, session_id)
    ensure_questions(db, session)
    refreshed = get_session_or_404(db, session_id)
    return {
        "session": serialize_session_detail(refreshed),
        "next_question": serialize_question(get_next_question(refreshed)),
    }


@router.get("/sessions/{session_id}/questions")
def get_questions(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = get_session_or_404(db, session_id)
    ensure_questions(db, session)
    refreshed = get_session_or_404(db, session_id)
    ordered_questions = sorted(refreshed.questions, key=lambda item: item.order_index)
    return {
        "items": [serialize_question(question) for question in ordered_questions],
        "next_question": serialize_question(get_next_question(refreshed)),
    }


@router.post("/sessions/{session_id}/answers")
def answer_question(session_id: int, request: AnswerRequest, db: Session = Depends(get_db)) -> dict:
    session = get_session_or_404(db, session_id)
    result = submit_answer(
        db=db,
        session=session,
        question_id=request.question_id,
        response_text=request.response_text,
    )
    refreshed = get_session_or_404(db, session_id)
    return {
        "submitted": result,
        "session": serialize_session_detail(refreshed),
        "next_question": serialize_question(get_next_question(refreshed)),
    }
