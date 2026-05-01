from sqlalchemy import select

from app.core.config import settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.entities import AssessmentSession
from app.services.seed import seed_demo_data


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    if not settings.seed_on_start:
        return

    with SessionLocal() as db:
        has_data = db.scalar(select(AssessmentSession.id).limit(1))
        if has_data:
            return
        seed_demo_data(db)
