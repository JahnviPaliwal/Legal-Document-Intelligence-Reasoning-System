"""
parser.py
Handles reading PDF files (or plain text) and splitting content into chunks
suitable for LLM processing.
"""

import os
import re


def read_file(file_path: str) -> str:
    """
    Reads a .txt file (or .pdf if PyPDF2 is available).
    Returns the extracted text as a string.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        try:
            import PyPDF2
            text_parts = []
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return "\n".join(text_parts)
        except ImportError:
            raise RuntimeError(
                "PyPDF2 is not installed. "
                "Install it with: pip install PyPDF2"
            )
    else:
        # Treat as plain text
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


def read_uploaded_file(uploaded_file) -> str:
    """
    Reads an uploaded Streamlit file object (UploadedFile).
    Supports .txt and .pdf.
    """
    name = uploaded_file.name.lower()
    raw_bytes = uploaded_file.read()

    if name.endswith(".pdf"):
        try:
            import PyPDF2
            import io
            reader = PyPDF2.PdfReader(io.BytesIO(raw_bytes))
            parts  = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    parts.append(text)
            return "\n".join(parts)
        except ImportError:
            # Fall back to treating bytes as text
            return raw_bytes.decode("utf-8", errors="ignore")
    else:
        return raw_bytes.decode("utf-8", errors="ignore")


def chunk_text(text: str,
               chunk_size: int = 1500,
               overlap: int = 200) -> list[str]:
    """
    Splits text into overlapping chunks so long documents fit in the LLM
    context window.

    Parameters
    ----------
    text       : full document text
    chunk_size : target characters per chunk
    overlap    : characters of overlap between consecutive chunks

    Returns
    -------
    list of text chunk strings
    """
    # Clean up extra whitespace
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    chunks  = []
    start   = 0
    length  = len(text)

    while start < length:
        end = min(start + chunk_size, length)

        # Try to break at a sentence boundary
        if end < length:
            # Look for ". " or "\n" near the end of the window
            boundary = text.rfind(". ", start, end)
            if boundary == -1:
                boundary = text.rfind("\n", start, end)
            if boundary != -1 and boundary > start:
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap  # step back by overlap for continuity

    return chunks
