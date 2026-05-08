from app.schemas.parser import (
    ParsedDocument,
    ParsedPage,
)


class MarkdownParser:

    @staticmethod
    def parse(
        file_path: str,
    ) -> ParsedDocument:

        with open(file_path,"r",encoding="utf-8",) as file:
            content = file.read()
            content = content.replace("\r\n","\n",)
            while "\n\n\n" in content:
                content = content.replace("\n\n\n","\n\n",)

        parsed_page = ParsedPage(page_number=1,text=content.strip(),)

        return ParsedDocument(pages=[parsed_page],total_pages=1,)