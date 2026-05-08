from pydantic import BaseModel


class ParsedPage(BaseModel):
    page_number: int
    text: str


class ParsedSection(BaseModel):
    title: str | None = None
    content: str
    page_number: int | None = None


class ParsedTable(BaseModel):
    title: str | None = None

    headers: list[str]

    rows: list[list[str]]

    page_number: int | None = None


class ParsedDocument(BaseModel):

    sections: list[ParsedSection]

    tables: list[ParsedTable]

    pages: list[ParsedPage]

    total_pages: int