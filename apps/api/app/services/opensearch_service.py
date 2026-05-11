from opensearchpy import (OpenSearch,)
from app.core.config import settings
from opensearchpy.helpers import (bulk,)

class OpenSearchService:

    INDEX_MAPPING = {
        "settings": {
            "index": {
                "knn": True,
            }
        },
        "mappings": {
            "properties": {
                "text": {
                    "type": "text"
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 768,
                    "method": {
                        "name": "hnsw",
                        "space_type": "cosinesimil",
                        "engine": "nmslib",
                    },
                },
                "metadata": {
                    "properties": {
                        "document_id": {
                            "type": "keyword"
                        },
                        "document_title": {
                            "type": "text"
                        },
                        "source_type": {
                            "type": "keyword"
                        },
                        "tenant_id": {
                            "type": "keyword"
                        },
                        "owner_id": {
                            "type": "keyword"
                        },
                        "page": {
                            "type": "integer"
                        },
                        "section": {
                            "type": "text"
                        },
                        "chunk_index": {
                            "type": "integer"
                        },
                        "chunk_type": {
                            "type": "keyword"
                        },
                    }
                },
            }
        },
    }

    client = OpenSearch(
        hosts=[
            {
                "host": (settings.OPENSEARCH_HOST),
                "port": (settings.OPENSEARCH_PORT),
            }
        ],
        http_auth=(settings.OPENSEARCH_USERNAME,settings.OPENSEARCH_PASSWORD,),
        use_ssl=False,
        verify_certs=False,
    )

    @staticmethod
    def create_index():

        index_name = (settings.OPENSEARCH_INDEX_NAME)

        exists = (OpenSearchService.client.indices.exists(index=index_name))

        if exists:
            print(f"Index already exists: "f"{index_name}")
            return

        OpenSearchService.client.indices.create(
            index=index_name,
            body=(OpenSearchService.INDEX_MAPPING),)

        print(f"Created index: "f"{index_name}")

    @staticmethod
    def delete_index():
        index_name = (settings.OPENSEARCH_INDEX_NAME)

        exists = (OpenSearchService.client.indices.exists(index=index_name))

        if exists:
            OpenSearchService.client.indices.delete(index=index_name)
            print(f"Deleted index: "f"{index_name}")

    @staticmethod
    def health_check():
        return (OpenSearchService.client.cluster.health())
    
    @staticmethod
    def bulk_index_chunks(chunk_embeddings,):
        actions = []

        for item in chunk_embeddings:
            chunk = item["chunk"]
            embedding = item["embedding"]
            action = {
                "_index": (
                    settings
                    .OPENSEARCH_INDEX_NAME
                ),
                "_id": (
                    f"{chunk.metadata.document_id}"
                    f"_{chunk.chunk_index}"
                ),
                "_source": {
                    "text": chunk.text,
                    "embedding": (
                        embedding
                    ),
                    "metadata": (
                        chunk.metadata
                        .model_dump()
                    ),
                },
            }

            actions.append(action)

        success, failed = bulk(
            OpenSearchService.client,
            actions,
        )

        print(f"Indexed {success} chunks")

        return {
            "success": success,
            "failed": failed,
        }