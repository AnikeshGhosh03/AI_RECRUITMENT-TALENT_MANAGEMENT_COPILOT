import os
from pathlib import Path
from typing import BinaryIO, Optional

import docx
import fitz


def extract_text_from_path(file_path: str | os.PathLike) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    if suffix == ".docx":
        return extract_text_from_docx(path)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {suffix}")


def extract_text_from_pdf(file_path: str | os.PathLike) -> str:
    document = fitz.open(file_path)
    text_chunks = [page.get_text() for page in document]
    document.close()
    return "\n".join(chunk.strip() for chunk in text_chunks if chunk and chunk.strip())


def extract_text_from_docx(file_path: str | os.PathLike) -> str:
    document = docx.Document(file_path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)


def extract_text_from_uploaded_file(uploaded_file: BinaryIO, filename: Optional[str] = None) -> str:
    suffix = Path(filename or "").suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_bytes(uploaded_file.read(), suffix=".pdf")
    if suffix == ".docx":
        return extract_text_from_bytes(uploaded_file.read(), suffix=".docx")
    if suffix == ".txt":
        return uploaded_file.read().decode("utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {suffix}")


def extract_text_from_bytes(file_bytes: bytes, suffix: str) -> str:
    if suffix == ".pdf":
        document = fitz.open(stream=file_bytes, filetype="pdf")
        text_chunks = [page.get_text() for page in document]
        document.close()
        return "\n".join(chunk.strip() for chunk in text_chunks if chunk and chunk.strip())
    if suffix == ".docx":
        import io

        document = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        return "\n".join(paragraphs)
    raise ValueError(f"Unsupported file type: {suffix}")
