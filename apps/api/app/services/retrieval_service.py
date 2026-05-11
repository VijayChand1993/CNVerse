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
    
    @staticmethod
    def hybrid_retrieve(
        query: str,
        top_k=10,
        tenant_id=None,
        owner_id=None,
        visibility=None,
        role=None,
    ):

        query_embedding = (
            EmbeddingService.embed_query(query))

        vector_results = (OpenSearchService.vector_search(
                                query_embedding=query_embedding,
                                top_k=top_k,
                                tenant_id=tenant_id,
                                owner_id=owner_id,
                                visibility=visibility,
                                role=role,
                                ))

        keyword_results = (OpenSearchService.keyword_search(
                                query_text=query,
                                top_k=top_k,
                                tenant_id=tenant_id,
                                owner_id=owner_id,
                                visibility=visibility,
                                role=role,
                                ))

        return (RetrievalService.merge_results(vector_results,keyword_results,))
    

    @staticmethod
    def merge_results(vector_results, keyword_results,):

        merged = {}
        for result in vector_results:
            doc_id = result["_id"]
            merged[doc_id] = {
                "result": result,
                "score": (
                    result["_score"] * 0.7
                ),
            }

        for result in keyword_results:
            doc_id = result["_id"]
            if doc_id in merged:
                merged[doc_id]["score"] += (result["_score"] * 0.3)
            else:
                merged[doc_id] = {"result": result,"score": (result["_score"] * 0.3),}

        sorted_results = sorted(
            merged.values(),
            key=lambda x: x["score"],
            reverse=True,
        )

        return [item["result"] for item in sorted_results]