
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from docling.chunking import HybridChunker
from docling_core.types.doc import DoclingDocument
from transformers import AutoTokenizer            # file path
from app.schemas.parser import (Chunk, ChunkMetadata)


def chunk_document(
    doc: DoclingDocument,
    source: str,
    tokenizer_name: str = "storage/models/all-MiniLM-L6-v2", #"sentence-transformers/all-MiniLM-L6-v2",
    max_tokens: int = 512,
) -> Iterator[Chunk]:
    """
    Uses Docling's HybridChunker — respects document structure AND
    stays within token limits for your embedding model.
    """
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, local_files_only=True,)
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=max_tokens,
        merge_peers=True,   # merges small sibling sections to avoid tiny chunks
    )

    for index, chunk in enumerate(chunker.chunk(doc)):
        meta = chunk.meta

        # Extract heading breadcrumb from the chunk's doc hierarchy
        headings = meta.headings or []

        # Page number from the first referenced item
        page = None
        if meta.doc_items:
            prov = meta.doc_items[0].prov
            if prov:
                page = prov[0].page_no

        yield Chunk(
            chunk_index=index,
            text=chunker.serialize(chunk),  # clean serialized text
            metadata= ChunkMetadata(
                section=" > ".join(headings),
                chunk_index=index,
                chunk_type="markdown",
                page=page,
                file=str(source),
                tenant_id=1,
                visibility="public",
                role="all",
                department="all"
            )
        )