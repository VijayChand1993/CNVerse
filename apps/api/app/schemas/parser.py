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

class ChunkMetadata(BaseModel):
    document_id: int | None = None
    document_title: str | None = None
    file: str | None = None
    source_type: str | None = None
    tenant_id: int | None = None
    owner_id: int | None = None
    page: int | None = None
    section: str | None = None
    chunk_index: int | None = None
    chunk_type: str | None = None
    visibility: str | None = None
    department: str | None = None
    role: str | None = None

class Chunk(BaseModel):
    chunk_index: int
    text: str
    metadata: ChunkMetadata