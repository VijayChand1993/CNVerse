from docx import Document as DocxDocument

from app.schemas.parser import (
    ParsedDocument,
    ParsedPage,
)


class DOCXParser:

    @staticmethod
    def parse(
        file_path: str,
    ) -> ParsedDocument:

        document = DocxDocument(file_path)

        parsed_pages = []

        extracted_content = []

        # Paragraphs
        for paragraph in document.paragraphs:

            text = paragraph.text.strip()
            style_name = (
                paragraph.style.name.lower()
            )

            if "heading" in style_name:
                extracted_content.append(
                    f"\n## {text}\n"
                )
            else:
                extracted_content.append(text)

        # Tables
        for table in document.tables:

            for row in table.rows:

                row_text = []

                for cell in row.cells:

                    cell_text = (
                        cell.text.strip()
                    )

                    if cell_text:
                        row_text.append(
                            cell_text
                        )

                if row_text:
                    extracted_content.append(
                        " | ".join(row_text)
                    )

        parsed_pages.append(
            ParsedPage(
                page_number=1,
                text="\n".join(
                    extracted_content
                ),
            )
        )

        return ParsedDocument(
            pages=parsed_pages,
            total_pages=len(parsed_pages),
        )