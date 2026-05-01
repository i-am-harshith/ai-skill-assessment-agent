from dataclasses import dataclass


@dataclass(frozen=True)
class SkillDefinition:
    name: str
    category: str
    synonyms: tuple[str, ...]
    concepts: tuple[str, ...]
    resources: tuple[dict, ...]


SKILL_CATALOG = [
    SkillDefinition(
        name="Python",
        category="Programming",
        synonyms=("python", "python3"),
        concepts=("asyncio", "typing", "pydantic", "virtualenv", "pytest", "packaging"),
        resources=(
            {"title": "Python Docs Tutorial", "url": "https://docs.python.org/3/tutorial/"},
            {"title": "Python Packaging User Guide", "url": "https://packaging.python.org/"},
        ),
    ),
    SkillDefinition(
        name="JavaScript",
        category="Programming",
        synonyms=("javascript", "js", "ecmascript"),
        concepts=("closure", "promise", "event loop", "async", "array methods", "modules"),
        resources=(
            {"title": "MDN JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
            {"title": "JavaScript.info", "url": "https://javascript.info/"},
        ),
    ),
    SkillDefinition(
        name="TypeScript",
        category="Programming",
        synonyms=("typescript", "ts"),
        concepts=("types", "interface", "generic", "union", "narrowing", "strict"),
        resources=(
            {"title": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html"},
            {"title": "TS Playground", "url": "https://www.typescriptlang.org/play"},
        ),
    ),
    SkillDefinition(
        name="SQL",
        category="Data",
        synonyms=("sql", "postgresql", "mysql", "sqlite"),
        concepts=("join", "index", "query plan", "normalization", "aggregate", "cte"),
        resources=(
            {"title": "PostgreSQL Tutorial", "url": "https://www.postgresql.org/docs/current/tutorial.html"},
            {"title": "SQLBolt", "url": "https://sqlbolt.com/"},
        ),
    ),
    SkillDefinition(
        name="React",
        category="Frontend",
        synonyms=("react", "reactjs", "react.js"),
        concepts=("hooks", "state", "props", "routing", "render", "context"),
        resources=(
            {"title": "React Learn", "url": "https://react.dev/learn"},
            {"title": "React Reference", "url": "https://react.dev/reference/react"},
        ),
    ),
    SkillDefinition(
        name="Next.js",
        category="Frontend",
        synonyms=("next.js", "nextjs", "next"),
        concepts=("app router", "server components", "ssr", "routes", "deployment", "data fetching"),
        resources=(
            {"title": "Next.js Learn", "url": "https://nextjs.org/learn"},
            {"title": "Next.js Docs", "url": "https://nextjs.org/docs"},
        ),
    ),
    SkillDefinition(
        name="Tailwind CSS",
        category="Frontend",
        synonyms=("tailwind", "tailwind css"),
        concepts=("utility classes", "responsive", "theme", "design system", "components", "states"),
        resources=(
            {"title": "Tailwind Docs", "url": "https://tailwindcss.com/docs"},
            {"title": "Tailwind Components Guide", "url": "https://tailwindcss.com/docs/reusing-styles"},
        ),
    ),
    SkillDefinition(
        name="FastAPI",
        category="Backend",
        synonyms=("fastapi",),
        concepts=("dependency injection", "pydantic", "async", "router", "validation", "swagger"),
        resources=(
            {"title": "FastAPI Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/"},
            {"title": "FastAPI Deployment", "url": "https://fastapi.tiangolo.com/deployment/"},
        ),
    ),
    SkillDefinition(
        name="Django",
        category="Backend",
        synonyms=("django",),
        concepts=("orm", "views", "migrations", "admin", "middleware", "rest"),
        resources=(
            {"title": "Django Intro", "url": "https://docs.djangoproject.com/en/stable/intro/"},
            {"title": "Django REST Framework", "url": "https://www.django-rest-framework.org/"},
        ),
    ),
    SkillDefinition(
        name="Node.js",
        category="Backend",
        synonyms=("node", "nodejs", "node.js"),
        concepts=("event loop", "express", "stream", "runtime", "npm", "middleware"),
        resources=(
            {"title": "Node.js Learn", "url": "https://nodejs.org/en/learn"},
            {"title": "Node.js Docs", "url": "https://nodejs.org/api/"},
        ),
    ),
    SkillDefinition(
        name="REST APIs",
        category="Backend",
        synonyms=("rest api", "restful", "api design", "rest"),
        concepts=("http", "status code", "pagination", "versioning", "idempotent", "contract"),
        resources=(
            {"title": "MDN HTTP Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP"},
            {"title": "Microsoft REST API Guidelines", "url": "https://github.com/microsoft/api-guidelines"},
        ),
    ),
    SkillDefinition(
        name="PostgreSQL",
        category="Data",
        synonyms=("postgresql", "postgres", "psql"),
        concepts=("index", "vacuum", "transactions", "schema", "jsonb", "query planner"),
        resources=(
            {"title": "PostgreSQL Docs", "url": "https://www.postgresql.org/docs/current/index.html"},
            {"title": "PostgreSQL Exercises", "url": "https://pgexercises.com/"},
        ),
    ),
    SkillDefinition(
        name="SQLite",
        category="Data",
        synonyms=("sqlite", "sqlite3"),
        concepts=("schema", "pragma", "transaction", "index", "foreign key", "wal"),
        resources=(
            {"title": "SQLite Docs", "url": "https://www.sqlite.org/docs.html"},
            {"title": "SQLite Tutorial", "url": "https://www.sqlitetutorial.net/"},
        ),
    ),
    SkillDefinition(
        name="Docker",
        category="DevOps",
        synonyms=("docker", "container", "containers"),
        concepts=("image", "container", "compose", "network", "volume", "registry"),
        resources=(
            {"title": "Docker Guides", "url": "https://docs.docker.com/guides/"},
            {"title": "Docker Compose", "url": "https://docs.docker.com/compose/"},
        ),
    ),
    SkillDefinition(
        name="AWS",
        category="Cloud",
        synonyms=("aws", "amazon web services", "s3", "lambda", "ec2"),
        concepts=("iam", "lambda", "s3", "cloudwatch", "ec2", "vpc"),
        resources=(
            {"title": "AWS Skill Builder", "url": "https://skillbuilder.aws/"},
            {"title": "AWS Documentation", "url": "https://docs.aws.amazon.com/"},
        ),
    ),
    SkillDefinition(
        name="CI/CD",
        category="DevOps",
        synonyms=("ci/cd", "cicd", "continuous integration", "continuous delivery"),
        concepts=("pipeline", "build", "deploy", "lint", "test automation", "rollback"),
        resources=(
            {"title": "GitHub Actions Docs", "url": "https://docs.github.com/en/actions"},
            {"title": "Azure CI/CD Concepts", "url": "https://learn.microsoft.com/en-us/devops/what-is-devops"},
        ),
    ),
    SkillDefinition(
        name="Testing",
        category="Quality",
        synonyms=("testing", "unit test", "integration test", "pytest", "jest", "qa"),
        concepts=("unit", "integration", "mock", "coverage", "regression", "e2e"),
        resources=(
            {"title": "Pytest Docs", "url": "https://docs.pytest.org/en/stable/"},
            {"title": "Testing Library Docs", "url": "https://testing-library.com/docs/"},
        ),
    ),
    SkillDefinition(
        name="System Design",
        category="Architecture",
        synonyms=("system design", "architecture", "distributed systems", "scalability"),
        concepts=("latency", "throughput", "cache", "queue", "tradeoff", "scaling"),
        resources=(
            {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer"},
            {"title": "AWS Architecture Center", "url": "https://aws.amazon.com/architecture/"},
        ),
    ),
    SkillDefinition(
        name="Git",
        category="Delivery",
        synonyms=("git", "github", "gitlab", "version control"),
        concepts=("branch", "merge", "rebase", "pull request", "commit", "conflict"),
        resources=(
            {"title": "Git Book", "url": "https://git-scm.com/book/en/v2"},
            {"title": "GitHub Docs", "url": "https://docs.github.com/en"},
        ),
    ),
    SkillDefinition(
        name="Machine Learning",
        category="AI",
        synonyms=("machine learning", "ml", "supervised learning", "classification"),
        concepts=("feature", "training", "validation", "model", "metric", "overfitting"),
        resources=(
            {"title": "scikit-learn Tutorials", "url": "https://scikit-learn.org/stable/tutorial/"},
            {"title": "Google ML Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"},
        ),
    ),
    SkillDefinition(
        name="Data Analysis",
        category="Data",
        synonyms=("data analysis", "analytics", "dashboard", "reporting"),
        concepts=("cleaning", "eda", "visualization", "insights", "metrics", "stakeholder"),
        resources=(
            {"title": "Pandas User Guide", "url": "https://pandas.pydata.org/docs/user_guide/index.html"},
            {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn"},
        ),
    ),
    SkillDefinition(
        name="OpenAI API",
        category="AI",
        synonyms=("openai", "gpt", "chatgpt api", "openai api"),
        concepts=("prompt", "completion", "response schema", "embedding", "tool calling", "tokens"),
        resources=(
            {"title": "OpenAI Platform Docs", "url": "https://platform.openai.com/docs/overview"},
            {"title": "OpenAI Quickstart", "url": "https://platform.openai.com/docs/quickstart"},
        ),
    ),
    SkillDefinition(
        name="Prompt Engineering",
        category="AI",
        synonyms=("prompt engineering", "prompt design", "instruction tuning", "few-shot"),
        concepts=("system prompt", "few-shot", "schema", "constraints", "examples", "evaluation"),
        resources=(
            {"title": "OpenAI Prompting Guide", "url": "https://platform.openai.com/docs/guides/text"},
            {"title": "Prompt Engineering Guide", "url": "https://www.promptingguide.ai/"},
        ),
    ),
    SkillDefinition(
        name="RAG",
        category="AI",
        synonyms=("rag", "retrieval augmented generation", "vector search", "retrieval"),
        concepts=("embedding", "chunking", "retrieval", "rerank", "vector db", "grounding"),
        resources=(
            {"title": "OpenAI RAG Cookbook", "url": "https://cookbook.openai.com/"},
            {"title": "Pinecone Learn RAG", "url": "https://www.pinecone.io/learn/"},
        ),
    ),
    SkillDefinition(
        name="NLP",
        category="AI",
        synonyms=("nlp", "natural language processing"),
        concepts=("tokenization", "classification", "embeddings", "entities", "semantic", "language model"),
        resources=(
            {"title": "spaCy Course", "url": "https://course.spacy.io/en/"},
            {"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course"},
        ),
    ),
    SkillDefinition(
        name="Communication",
        category="Collaboration",
        synonyms=("communication", "stakeholder management", "collaboration", "cross-functional"),
        concepts=("stakeholder", "clarity", "alignment", "handoff", "facilitation", "documentation"),
        resources=(
            {"title": "Atlassian Communication Guide", "url": "https://www.atlassian.com/team-playbook/plays/project-kickoff"},
            {"title": "Write the Docs Guide", "url": "https://www.writethedocs.org/guide/"},
        ),
    ),
    SkillDefinition(
        name="Problem Solving",
        category="Collaboration",
        synonyms=("problem solving", "analytical thinking", "troubleshooting", "debugging"),
        concepts=("root cause", "tradeoff", "hypothesis", "experiments", "metrics", "decision"),
        resources=(
            {"title": "Google SRE Workbook", "url": "https://sre.google/workbook/table-of-contents/"},
            {"title": "The Debugging Book", "url": "https://www.debuggingbook.org/"},
        ),
    ),
]

SKILL_LOOKUP = {skill.name: skill for skill in SKILL_CATALOG}
