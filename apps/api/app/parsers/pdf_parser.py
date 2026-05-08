import fitz
import pdfplumber

from app.schemas.parser import (
    ParsedDocument,
    ParsedPage,
)


class PDFParser:

    @staticmethod
    def parse_with_pdfplumber(
        file_path: str,
    ) -> ParsedDocument:

        parsed_pages = []

        with pdfplumber.open(file_path) as pdf:

            for index, page in enumerate(pdf.pages):

                text = page.extract_text() or ""

                parsed_pages.append(
                    ParsedPage(
                        page_number=index + 1,
                        text=text.strip(),
                    )
                )

        return ParsedDocument(
            pages=parsed_pages,
            total_pages=len(parsed_pages),
        )

    @staticmethod
    def parse_with_pymupdf(
        file_path: str,
    ) -> ParsedDocument:

        parsed_pages = []

        document = fitz.open(file_path)

        for index, page in enumerate(document):

            text = page.get_text()

            parsed_pages.append(
                ParsedPage(
                    page_number=index + 1,
                    text=text.strip(),
                )
            )

        return ParsedDocument(
            pages=parsed_pages,
            total_pages=len(parsed_pages),
        )

    @staticmethod
    def parse(
        file_path: str,
    ) -> ParsedDocument:

        try:

            parsed_document = (
                PDFParser.parse_with_pdfplumber(
                    file_path
                )
            )

            extracted_text = "".join(
                [
                    page.text
                    for page in parsed_document.pages
                ]
            )

            if extracted_text.strip():
                return parsed_document

        except Exception as exc:
            print(
                f"pdfplumber failed: {exc}"
            )

        print(
            "Falling back to pymupdf..."
        )

        return PDFParser.parse_with_pymupdf(
            file_path
        )