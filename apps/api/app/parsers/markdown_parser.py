from app.schemas.parser import (
    ParsedDocument,
    ParsedPage,
    ParsedSection,
)


class MarkdownParser:

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

            lines = content.split("\n")

            parsed_sections = []

            current_title = "Introduction"

            current_content = []

            for line in lines:

                stripped_line = line.strip()

                if stripped_line.startswith("#"):

                    if current_content:

                        parsed_sections.append(
                            ParsedSection(
                                title=current_title,
                                content="\n".join(
                                    current_content
                                ),
                                page_number=1,
                            )
                        )

                    current_title = (
                        stripped_line.lstrip("#").strip()
                    )

                    current_content = []

                else:
                    current_content.append(line)

            if current_content:

                parsed_sections.append(
                    ParsedSection(
                        title=current_title,
                        content="\n".join(
                            current_content
                        ),
                        page_number=1,
                    )
                )

            parsed_page = ParsedPage(
                page_number=1,
                text=content.strip(),
            )

            return ParsedDocument(
                sections=parsed_sections,
                tables=[],
                pages=[parsed_page],
                total_pages=1,
            )

        except Exception as exc:
            raise ValueError(
                f"Markdown parsing failed: {exc}"
            )