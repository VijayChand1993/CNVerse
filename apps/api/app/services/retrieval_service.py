from app.services.embedding_service import (EmbeddingService,)
from app.services.opensearch_service import (OpenSearchService,)


class RetrievalService:

    @staticmethod
    def retrieve(
        query: str,
        tenant_id=None,
        owner_id=None,
        visibility=None,
        role=None,
    ):
        query_embedding = (
            EmbeddingService.embed_query(query))

        results = (
            OpenSearchService
            .vector_search(
                query_embedding=query_embedding,
                tenant_id=tenant_id,
                owner_id=owner_id,
                visibility=visibility,
                role=role,
            )
        )

        return results