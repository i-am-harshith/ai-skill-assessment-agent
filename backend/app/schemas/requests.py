from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    job_description_id: int
    resume_id: int
    session_name: str | None = None


class AnswerRequest(BaseModel):
    question_id: int
    response_text: str = Field(min_length=10)
