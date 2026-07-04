from pages.core.parser.file_handler import extract_text_from_pdf


def extract_pdf_text(file_path: str) -> str:
    return extract_text_from_pdf(file_path)
