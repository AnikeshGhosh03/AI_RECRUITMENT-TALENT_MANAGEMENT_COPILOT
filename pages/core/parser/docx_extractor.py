from pages.core.parser.file_handler import extract_text_from_docx


def extract_docx_text(file_path: str) -> str:
    return extract_text_from_docx(file_path)
