from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.assessment_engine import get_session_or_404, list_catalog, list_sessions
from app.utils.serializers import serialize_session_detail

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.get("/catalog")
def get_catalog(db: Session = Depends(get_db)) -> dict:
    return list_catalog(db)


@router.get("/sessions")
def get_sessions(db: Session = Depends(get_db)) -> dict:
    return {"items": list_sessions(db)}


@router.get("/sessions/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = get_session_or_404(db, session_id)
    return serialize_session_detail(session)


@router.get("/sessions/{session_id}/analysis")
def get_analysis(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = get_session_or_404(db, session_id)
    return serialize_session_detail(session)


@router.get("/sessions/{session_id}/report")
def get_report(session_id: int, db: Session = Depends(get_db)) -> dict:
    session = get_session_or_404(db, session_id)
    if not session.skill_assessments:
        raise HTTPException(status_code=404, detail="Session analysis not found.")
    return serialize_session_detail(session)
