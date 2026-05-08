
from app.parsers.docling_parser import (DoclingParser)

class ParsingService:

    @staticmethod
    def parse_document(
        file_path: str,
    ):
        try:
            parser = DoclingParser()
            return parser.parse(file_path=file_path)
        except Exception as exc:
            raise ValueError(f"Docling parsing failed: {exc}")
