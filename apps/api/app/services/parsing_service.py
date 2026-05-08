from pathlib import Path

from app.parsers.pdf_parser import PDFParser
from app.parsers.docx_parser import (DOCXParser)
from app.parsers.xlsx_parser import (XLSXParser)
from app.parsers.markdown_parser import (MarkdownParser)
from app.parsers.text_parser import (TextParser)


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
        
        if extension == ".docx":
            try:
                return DOCXParser.parse(file_path)
            except Exception as exc:
                raise ValueError(f"DOCX parsing failed: {exc}")
        if extension == ".xlsx":
            try:
                return XLSXParser.parse(file_path)
            except Exception as exc:
                raise ValueError(f"Excel parsing failed: {exc}")
        if extension == ".md":
            try:
                return MarkdownParser.parse(file_path)
            except Exception as exc:
                raise ValueError(f"Markdown parsing failed: {exc}")
        if extension == ".txt":
            try:
                return TextParser.parse(file_path)
            except Exception as exc:
                raise ValueError(f"Text parsing failed: {exc}")
            

        raise ValueError(
            f"Unsupported file type: {extension}"
        )