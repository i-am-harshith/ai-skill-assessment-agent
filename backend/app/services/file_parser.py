from io import BytesIO
from pathlib import Path

from docx import Document
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def _extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join((page.extract_text() or "").strip() for page in reader.pages).strip()


def _extract_docx_text(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()


async def resolve_text_payload(file: UploadFile | None, raw_text: str | None) -> tuple[str, str, str | None]:
    manual_text = (raw_text or "").strip()
    if manual_text:
        return manual_text, "text", None

    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Provide either manual text input or a supported file upload.")

    extension = Path(file.filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        if extension == ".txt":
            content = file_bytes.decode("utf-8", errors="ignore").strip()
        elif extension == ".pdf":
            content = _extract_pdf_text(file_bytes)
        else:
            content = _extract_docx_text(file_bytes)
    except Exception as exc:  # pragma: no cover - defensive path for parser errors
        raise HTTPException(status_code=400, detail=f"Could not parse the uploaded file: {exc}") from exc

    if not content:
        raise HTTPException(status_code=400, detail="No readable text was found in the uploaded file.")

    return content, extension.lstrip("."), file.filename
