import os
import shutil
from pathlib import Path

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
)
from app.utils.download import download_file

from app.services.queue_service import QueueService

from app.services.parsing_service import (
    ParsingService,
)

router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
)


@router.post(
    "/upload",
    response_model=UploadResponse,
)
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

    sha256_hash = generate_sha256(str(file_path))

    existing_document = DocumentService.get_by_sha256(
        db=db,
        sha256_hash=sha256_hash,
    )

    if existing_document:
        os.remove(file_path)

        raise HTTPException(
            status_code=409,
            detail="Duplicate document detected",
        )

    document = Document(
        title=file.filename,
        source_type="upload",
        source_url=str(file_path),
        sha256_hash=sha256_hash,
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

@router.post(
    "/url",
    response_model=URLIngestionResponse,
)
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

    sha256_hash = generate_sha256(str(file_path))

    existing_document = DocumentService.get_by_sha256(
        db=db,
        sha256_hash=sha256_hash,
    )

    if existing_document:
        os.remove(file_path)

        raise HTTPException(
            status_code=409,
            detail="Duplicate document detected",
        )

    document = Document(
        title=filename,
        source_type="url",
        source_url=str(payload.url),
        sha256_hash=sha256_hash,
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
async def parse_test(
    file: UploadFile = File(...),
):

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

    if not parsed_document.pages:
        raise ValueError(
            "No content extracted"
        )

    return parsed_document