import logfire

def parse_text(file_path: str):
    """
    Parses text content from a file.
    Cleans and extracts readable text for RAG.
    """
    with logfire.span("📄 Text Parsing", filename=file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logfire.error(f"Error parsing text file {file_path}: {e}")
            raise e