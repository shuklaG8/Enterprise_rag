from bs4 import BeautifulSoup
import logfire


def parse_html(file_path: str) -> str:
    """
    Parse HTML content using BeautifulSoup.

    Removes non-content HTML elements and returns
    clean readable text for the RAG ingestion pipeline.
    """

    with logfire.span("📄 HTML Parsing", filename=file_path):
        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                content = f.read()

            # Parse HTML
            soup = BeautifulSoup(content, "html.parser")

            # Remove non-readable elements
            for tag in soup(
                ["script", "style", "meta", "noscript", "svg"]
            ):
                tag.decompose()

            # Extract text directly as STRING
            text = soup.get_text(
                separator="\n",
                strip=True,
            )

            # Clean each line
            cleaned_lines = []

            for line in text.splitlines():
                line = line.strip()

                if not line:
                    continue

                # Normalize multiple spaces
                line = " ".join(line.split())

                cleaned_lines.append(line)

            # Final string
            text_clean = "\n".join(cleaned_lines)

            if not text_clean:
                logfire.warning(
                    f"No readable text extracted from {file_path}"
                )

            # IMPORTANT: guarantee string
            return text_clean

        except Exception as e:
            logfire.error(
                f"Error parsing HTML file {file_path}: {e}"
            )
            raise