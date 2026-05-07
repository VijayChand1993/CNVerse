from pydantic import BaseModel, HttpUrl


class UploadResponse(BaseModel):
    document_id: int
    ingestion_job_id: int
    filename: str
    status: str

class URLIngestionRequest(BaseModel):
    url: HttpUrl = "https://ontheline.trincoll.edu/images/bookdown/sample-local-pdf.pdf"

class URLIngestionResponse(BaseModel):
    document_id: int
    ingestion_job_id: int
    filename: str
    source_url: str
    status: str