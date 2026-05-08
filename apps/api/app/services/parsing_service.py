from pathlib import Path

from app.parsers.pdf_parser import PDFParser


class ParsingService:

    @staticmethod
    def parse_document(
        file_path: str,
    ):

        extension = (
            Path(file_path)
            .suffix
            .lower()
        )

        if extension == ".pdf":
            return PDFParser.parse(file_path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )