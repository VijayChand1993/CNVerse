import os
import shutil
from pathlib import Path

from app.services.opensearch_service import OpenSearchService
from app.services.retrieval_service import RetrievalService
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import ALLOWED_EXTENSIONS
from app.db.dependencies import get_db
from app.models.document import (
    Document,
    DocumentStatus,
    DocumentVisibility,
)
from app.models.ingestion_job import (
    IngestionJob,
    IngestionJobStatus,
    IngestionJobType,
)
from app.schemas.ingestion import UploadResponse
from app.services.document_service import DocumentService
from app.services.ingestion_job_service import (
    IngestionJobService,
)
from app.utils.file import (
    generate_sha256,
    get_file_extension,
)

from urllib.parse import urlparse

from app.schemas.ingestion import (
    URLIngestionRequest,
    URLIngestionResponse,
    DuplicateDocumentResponse
)
from app.utils.download import download_file

from app.services.queue_service import QueueService

from app.services.parsing_service import (
    ParsingService,
)

from app.services.deduplication_service import (
    DeduplicationService,
)
from app.parsers.docling_parser import (DoclingParser, ParseResult)
from app.schemas.parser import (ParsedDocument)
from app.chunkers.markdown_chunker import (chunk_document, Chunk)
from app.services.embedding_service import EmbeddingService
from app.services.chunking_service import ChunkService
from app.services.embedding_service import (EmbeddingService,)
from app.services.indexing_service import (IndexingService,)

router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
)


@router.post("/upload", response_model=UploadResponse,)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    extension = get_file_extension(file.filename)

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type",
        )

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    dedup_result = (
        DeduplicationService.check_duplicate(
            db=db,
            file_path=str(file_path),
        )
    )

    if dedup_result["is_duplicate"]:
        os.remove(file_path)

        raise HTTPException(
            status_code=409,
            detail=DuplicateDocumentResponse(
                message="Duplicate document detected",
                document_id=dedup_result["document"].id
            ).model_dump()
        )

    document = Document(
        title=file.filename,
        source_type="upload",
        source_url=str(file_path),
        sha256_hash=dedup_result["sha256_hash"],
        status=DocumentStatus.PENDING.value,
        visibility=DocumentVisibility.PRIVATE.value,
    )

    document = DocumentService.create_document(
        db=db,
        document=document,
    )

    ingestion_job = IngestionJob(
        job_type=IngestionJobType.UPLOAD.value,
        status=IngestionJobStatus.PENDING.value,
        total_documents=1,
    )

    ingestion_job = IngestionJobService.create_job(
        db=db,
        job=ingestion_job,
    )

    QueueService.enqueue_ingestion_job({
        "document_id": document.id,
        "ingestion_job_id": ingestion_job.id,
        "retry_count": 0
    })

    return UploadResponse(
        document_id=document.id,
        ingestion_job_id=ingestion_job.id,
        filename=file.filename,
        status=document.status,
    )

@router.post("/url",response_model=URLIngestionResponse,)
async def ingest_from_url(
    payload: URLIngestionRequest,
    db: Session = Depends(get_db),
):

    parsed_url = urlparse(str(payload.url))

    filename = Path(parsed_url.path).name

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid file URL",
        )

    extension = get_file_extension(filename)

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type",
        )

    download_dir = Path(settings.URL_DOWNLOAD_DIR)

    download_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = download_dir / filename

    try:
        await download_file(
            url=str(payload.url),
            destination=str(file_path),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download file: {str(exc)}",
        )

    dedup_result = (
        DeduplicationService.check_duplicate(
            db=db,
            file_path=str(file_path),
        )
    )

    if dedup_result["is_duplicate"]:
        os.remove(file_path)

        raise HTTPException(
            status_code=409,
            detail=DuplicateDocumentResponse(
                message="Duplicate document detected",
                document_id=dedup_result["document"].id
            ).model_dump()
        )

    document = Document(
        title=filename,
        source_type="url",
        source_url=str(payload.url),
        sha256_hash=dedup_result["sha256_hash"],
        status=DocumentStatus.PENDING.value,
        visibility=DocumentVisibility.PUBLIC.value,
    )

    document = DocumentService.create_document(
        db=db,
        document=document,
    )

    ingestion_job = IngestionJob(
        job_type=IngestionJobType.URL.value,
        status=IngestionJobStatus.PENDING.value,
        total_documents=1,
    )

    ingestion_job = IngestionJobService.create_job(
        db=db,
        job=ingestion_job,
    )

    QueueService.enqueue_ingestion_job({
        "document_id": document.id,
        "ingestion_job_id": ingestion_job.id,
        "retry_count": 0
    })

    return URLIngestionResponse(
        document_id=document.id,
        ingestion_job_id=ingestion_job.id,
        filename=filename,
        source_url=str(payload.url),
        status=document.status,
    )

@router.post("/parse-test")
async def parse_test(file: UploadFile = File(...),):

    temp_dir = Path("./storage/temp")

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = temp_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    parsed_document = (
        ParsingService.parse_document(
            str(file_path)
        )
    )

    if type(parsed_document) is ParseResult and not parsed_document.document:
        raise ValueError("No content extracted")

    return parsed_document

@router.post("/parse-chunk-test")
async def parse_chunk_test(file: UploadFile = File(...),):
    temp_dir = Path("./storage/temp")

    temp_dir.mkdir(parents=True, exist_ok=True,)

    file_path = temp_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj( file.file, buffer,)

    parsed_document = (
        ParsingService.parse_document(str(file_path)))

    if type(parsed_document) is ParseResult and not parsed_document.document:
        raise ValueError("No content extracted")
    
    if type(parsed_document) is ParseResult:
        if parsed_document.success:
            chunks = ChunkService.chunk_docling_document(parsed_document.document, parsed_document.file_path)

    return chunks

@router.post("/embed-test")
async def embed_test():

    sample_text = (
        "Employees are entitled "
        "to 20 annual leave days."
    )

    embedding = (
        EmbeddingService.embed_documents(
            [sample_text]
        )
    )

    return {
        "dimension": len(
            embedding[0]
        ),
        "embedding_preview": (
            embedding[0][:10]
        ),
    }

@router.get("/opensearch-health")
async def opensearch_health():

    return (
        OpenSearchService.health_check()
    )

@router.post("/index-test")
async def index_test(file: UploadFile = File(...),):
    temp_dir = Path("temp")
    temp_dir.mkdir(parents=True,exist_ok=True,)

    file_path = (temp_dir / file.filename)

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file,buffer,)

    parser = DoclingParser()
    parse_result = (parser.parse(str(file_path)))

    print(parse_result)

    chunks = (
        ChunkService.chunk_docling_document(parse_result.document, file_path))

    result = (IndexingService.index_chunks(chunks))

    return {
        "chunks": len(chunks),
        "indexing_result": result,
    }

@router.get("/search-test")
async def search_test():

    results = (
        RetrievalService.retrieve(
            query="leave policy",
            tenant_id=1,
            visibility="public",
        )
    )

    return results

@router.get("/hybrid-search")
async def hybrid_search():

    results = (
        RetrievalService
        .hybrid_retrieve(
            query="leave policy",
            tenant_id=1,
            visibility="public",
        )
    )
    return results

@router.get("/rerank-search")
async def rerank_search():

    results = (
        RetrievalService
        .hybrid_retrieve(
            query="work from home policy",
            tenant_id=1,
            visibility="public",
        )
    )

    return results