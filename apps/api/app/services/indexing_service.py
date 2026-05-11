from app.services.embedding_service import (EmbeddingService,)
from app.services.opensearch_service import (OpenSearchService,)
from app.schemas.parser import (Chunk,)
from app.core.config import settings


class IndexingService:
    @staticmethod
    def index_chunks(chunks: list[Chunk],):
        chunk_embeddings = (
            EmbeddingService.embed_chunks(chunks))

        result = (OpenSearchService.bulk_index_chunks(chunk_embeddings))
        OpenSearchService.client.indices.refresh(index=settings.OPENSEARCH_INDEX_NAME)

        return result