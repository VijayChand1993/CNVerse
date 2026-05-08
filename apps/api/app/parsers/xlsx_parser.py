from openpyxl import load_workbook

from app.schemas.parser import (
    ParsedDocument,
    ParsedPage,
)


class XLSXParser:

    @staticmethod
    def parse(
        file_path: str,
    ) -> ParsedDocument:

        workbook = load_workbook(
            filename=file_path,
            data_only=True,
        )

        parsed_pages = []

        page_number = 1

        for sheet in workbook.worksheets:

            extracted_rows = []

            extracted_rows.append(
                f"## Sheet: {sheet.title}"
            )

            rows = list(sheet.iter_rows(values_only=True))

            for index, row in enumerate(rows):

                cleaned_row = []

                for cell in row:

                    if cell is None:
                        cleaned_row.append("")
                    else:
                        cleaned_row.append(
                            str(cell).strip()
                        )

                if any(cleaned_row):

                    row_text = " | ".join(cleaned_row)

                    if index == 0:
                        extracted_rows.append(f"HEADER: {row_text}")
                    else:
                        extracted_rows.append(row_text)

            parsed_pages.append(
                ParsedPage(
                    page_number=page_number,
                    text="\n".join(
                        extracted_rows
                    ),
                )
            )

            page_number += 1

        return ParsedDocument(
            pages=parsed_pages,
            total_pages=len(parsed_pages),
        )