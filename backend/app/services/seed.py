from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.entities import JobDescription, Resume
from app.services.assessment_engine import create_or_refresh_analysis_session, ensure_questions, get_session_or_404, submit_answer


def create_job_description_record(
    db: Session,
    title: str,
    company: str | None,
    raw_text: str,
    source_type: str,
    file_name: str | None = None,
) -> JobDescription:
    record = JobDescription(
        title=title,
        company=company,
        raw_text=raw_text.strip(),
        source_type=source_type,
        file_name=file_name,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_resume_record(
    db: Session,
    candidate_name: str,
    headline: str | None,
    raw_text: str,
    source_type: str,
    file_name: str | None = None,
) -> Resume:
    record = Resume(
        candidate_name=candidate_name,
        headline=headline,
        raw_text=raw_text.strip(),
        source_type=source_type,
        file_name=file_name,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


FULLSTACK_JD = """
Senior AI Product Engineer
Company: Northstar Labs

We are hiring an engineer to build AI-powered internal products and customer-facing workflows.
Must have strong Python, FastAPI, SQL, React, Tailwind CSS, REST API design, and Docker skills.
You should have hands-on experience integrating OpenAI or similar LLM APIs, prompt engineering,
retrieval-augmented generation (RAG), and production debugging.
Experience with AWS, CI/CD, testing, and cross-functional communication is required.
Nice to have: PostgreSQL, system design, analytics, and shipping zero-to-one prototypes.
"""

FULLSTACK_RESUME = """
Sarah Chen
Product-minded Full-Stack Engineer

Built internal AI copilots and workflow tools using Python, FastAPI, React, Tailwind CSS, SQLite, Docker, and AWS.
Implemented prompt engineering patterns, retrieval-augmented generation (RAG) workflows, and structured output validation for GPT-based features used by support and operations teams.
Designed REST APIs, background jobs, SQL reporting flows, and CI/CD pipelines for product experiments.
Led a migration from spreadsheets to a web platform, improving turnaround time by 38% through strong problem solving and system design trade-offs.
Collaborated with design, GTM, and operations teams, wrote release documentation, and ran sprint demos with clear communication.
Worked with PostgreSQL and testing via pytest coverage for critical paths.
"""

DATA_ANALYST_JD = """
Data Analyst
Company: Insight Forge

Required skills include SQL, Python, data analysis, dashboards, stakeholder communication, and testing data quality.
Strong experience with analytics, experimentation, reporting, and business storytelling is required.
Preferred: machine learning, AWS, and automation.
"""

DATA_ANALYST_RESUME = """
Rahul Verma
Analytics Specialist

Built weekly dashboards and reporting packs using SQL, Excel, and Tableau for finance and operations teams.
Cleaned datasets, wrote analysis notes, and communicated findings to stakeholders.
Some exposure to Python notebooks and basic AWS data workflows.
"""

FRONTEND_JD = """
Frontend Engineer
Company: Aurora Commerce

We need strong React, TypeScript, Next.js, Tailwind CSS, testing, performance optimisation, and accessibility.
Experience with APIs, CI/CD, Git, and communication across product/design is required.
"""

FRONTEND_RESUME = """
Maya Patel
Frontend Developer

Built responsive web apps using React, JavaScript, Tailwind CSS, and Git.
Worked closely with designers, shipped marketing pages, and improved Lighthouse performance scores.
Used REST APIs and component libraries, but limited production TypeScript and automated testing exposure.
"""


def seed_demo_data(db: Session) -> None:
    job_records = [
        create_job_description_record(db, "Senior AI Product Engineer", "Northstar Labs", FULLSTACK_JD, "seed"),
        create_job_description_record(db, "Data Analyst", "Insight Forge", DATA_ANALYST_JD, "seed"),
        create_job_description_record(db, "Frontend Engineer", "Aurora Commerce", FRONTEND_JD, "seed"),
    ]
    resume_records = [
        create_resume_record(db, "Sarah Chen", "Product-minded Full-Stack Engineer", FULLSTACK_RESUME, "seed"),
        create_resume_record(db, "Rahul Verma", "Analytics Specialist", DATA_ANALYST_RESUME, "seed"),
        create_resume_record(db, "Maya Patel", "Frontend Developer", FRONTEND_RESUME, "seed"),
    ]

    demo_session = create_or_refresh_analysis_session(
        db=db,
        job_description_id=job_records[0].id,
        resume_id=resume_records[0].id,
        session_name="Seeded Demo Session",
    )
    ensure_questions(db, demo_session)
    refreshed = get_session_or_404(db, demo_session.id)
    sample_answers = {
        "Python": "I built a Python service layer for an AI operations platform using typed service modules, pydantic validation, and pytest coverage. I split prompt orchestration, persistence, and evaluation into separate modules so we could test failures independently and ship changes safely.",
        "FastAPI": "In FastAPI I normally create routers by domain, use dependency injection for database sessions and auth, validate request and response models with Pydantic, and add middleware plus structured logs for observability. On one project this reduced debugging time because every failed request had enough context.",
        "React": "I built a React admin workflow with route-level code splitting, reusable form components, optimistic updates, and simple state lifting instead of over-engineering global state. I tracked drop-off on the review step and improved completion by redesigning the interaction flow.",
        "OpenAI API": "For LLM features I define prompt templates with strict output schemas, keep example inputs for regression checks, add retries with fallback handling, and log token usage per workflow. That helped us control spend and keep the assistant reliable for operations teams.",
        "Docker": "I containerised both frontend and backend services with small base images, environment-specific configs, and docker compose for local parity. We used separate build stages so deploy images stayed small and startup stayed predictable.",
        "SQL": "I wrote SQL for product and support analytics using joins, CTEs, and indexes on the highest-volume tables. When one report slowed down, I checked the query plan, added the right composite index, and cut runtime from minutes to seconds.",
        "REST APIs": "I design REST APIs around clear resource boundaries, response schemas, and predictable status codes. In production I added pagination, idempotent update patterns, and structured error payloads so both frontend and support teams could integrate without ambiguity.",
        "Tailwind CSS": "I use Tailwind CSS to build consistent component systems quickly, but I still define reusable patterns for spacing, states, and responsive layouts. On one internal product this let us move fast without losing visual consistency across the workflow screens.",
        "RAG": "I built a RAG workflow that chunked internal docs, generated embeddings, retrieved the best matching context, and passed grounded snippets into the final prompt. We evaluated answer quality against known references and tuned chunk size plus retrieval thresholds to reduce hallucinations.",
        "AWS": "I deployed product services on AWS using S3 for assets, EC2 or container workloads for app hosting, IAM for access control, and CloudWatch for monitoring. I usually start with the simplest reliable setup and only add complexity when traffic or compliance needs justify it.",
        "CI/CD": "I set up CI/CD pipelines to run linting, tests, and deployment checks before release. That reduced regressions because every merge had automated validation and a clear rollback path.",
        "Prompt Engineering": "I treat prompt engineering as product design plus evaluation. I define strict system instructions, few-shot examples, output constraints, and regression cases so the model stays reliable across common edge cases.",
        "Communication": "I keep communication practical: translate technical options into product impact, document decisions, and run short demos so design, operations, and engineering stay aligned. That helped us move faster because stakeholders understood trade-offs early.",
        "Problem Solving": "When an issue appears, I start with hypotheses, logs, and user impact. I narrow the failure path quickly, confirm the root cause with data, and then choose the smallest safe fix before scaling up the solution.",
        "Testing": "I rely on targeted unit and integration tests around the highest-risk paths. For one AI workflow I added regression cases for parsing, schema validation, and fallback behavior so changes were safer to ship.",
    }

    refreshed = get_session_or_404(db, demo_session.id)
    for question in sorted(refreshed.questions, key=lambda item: item.order_index):
        skill_name = question.skill_assessment.skill_name
        submit_answer(db, refreshed, question.id, sample_answers.get(skill_name, f"I have practical experience with {skill_name} in product delivery work."))
        refreshed = get_session_or_404(db, demo_session.id)
