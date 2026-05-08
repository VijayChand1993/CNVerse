from app.schemas.parser import (
    ParsedDocument,
    ParsedPage,
    ParsedSection,
)


class TextParser:

    @staticmethod
    def parse(
        file_path: str,
    ) -> ParsedDocument:

        try:

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                ) as file:

                    content = file.read()

            except UnicodeDecodeError:

                with open(
                    file_path,
                    "r",
                    encoding="latin-1",
                ) as file:

                    content = file.read()

            content = content.replace(
                "\r\n",
                "\n",
            )

            while "\n\n\n" in content:

                content = content.replace(
                    "\n\n\n",
                    "\n\n",
                )

            parsed_page = ParsedPage(
                page_number=1,
                text=content.strip(),
            )

            parsed_section = ParsedSection(
                title="Text Document",
                content=content.strip(),
                page_number=1,
            )

            return ParsedDocument(
                sections=[parsed_section],
                tables=[],
                pages=[parsed_page],
                total_pages=1,
            )

        except Exception as exc:
            raise ValueError(
                f"Text parsing failed: {exc}"
            )