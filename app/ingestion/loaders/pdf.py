import logfire
from pypdf import PdfReader

def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF locally using pypdf.
    Falls back to pdfplumber for pages that yield no text (e.g. image-heavy pages).
    """
    with logfire.span("PDF Parsing (local)", filename=file_path):
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            logfire.info(f"PDF has {total_pages} pages.")

            text_parts: list[str] = []
            blank_pages: list[int] = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    text_parts.append(text)
                else:
                    blank_pages.append(i + 1)  # Store 1-based page number

            if blank_pages:
                logfire.info(f"Pages with no text: {blank_pages}. Consider using pdfplumber for these pages.")
                try:
                    import pdfplumber
                    with pdfplumber.open(file_path) as pdf:
                        for page_num in blank_pages:
                            page = pdf.pages[page_num - 1]
                            fallback_text = page.extract_text() or ""
                            if fallback_text.strip():
                                text_parts.append(fallback_text)
                except Exception as plumber_err:
                    logfire.error(f"Failed to extract text from blank pages using pdfplumber: {plumber_err}")   

            full_text = "\n".join(text_parts)

            if not full_text.strip():
                logfire.warning("No text could be extracted from the PDF.")
            else:
                logfire.info(f"Extracted text length: {len(full_text)} characters.")

            return full_text

        except Exception as e:
            logfire.error(f"Failed to parse PDF: {e}")
            return ""                             