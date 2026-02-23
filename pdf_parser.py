import re
from typing import Optional

import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file and returns a cleaned plain string.

    Responsibilities:
    - Open PDF safely
    - Extract text page by page
    - Normalize whitespace
    - Return a single consolidated string
    """

    text_chunks = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text: Optional[str] = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    raw_text = "\n".join(text_chunks)

    return _clean_text(raw_text)


def _clean_text(text: str) -> str:
    """
    Cleans extracted PDF text:
    - Removes excessive whitespace
    - Normalizes line breaks
    - Strips leading/trailing spaces
    """

    # Normalize Windows/Mac line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove multiple blank lines
    text = re.sub(r"\n{2,}", "\n\n", text)

    # Collapse excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()
