"""
resume_parser.py
Single source of truth for PDF text extraction.
Uses PyMuPDF (fitz) — replaces the duplicate pdf_parser.py (pdfplumber).
Delete pdf_parser.py — keep only this file.
"""
 
import fitz  # PyMuPDF
 
 
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all text from a PDF given its raw bytes.
    Raises an Exception if the PDF cannot be read.
    """
    if not file_bytes:
        raise ValueError("No file bytes provided.")
 
    text = ""
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")
 
    result = text.strip()
    if not result:
        raise ValueError("PDF appears to be empty or unreadable (possibly scanned image).")
 
    return result
 