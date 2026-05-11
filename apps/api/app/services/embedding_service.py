# from sentence_transformers import SentenceTransformer

# class EmbeddingService:
#     model = SentenceTransformer("storage/models/Qwen3-Embedding-0.6B", local_files_only=True)

#     @staticmethod
#     def embed_texts(
#         texts: list[str],
#     ):
#         # For embedding queries — instruction improves retrieval 1-5%
#         return (
#             EmbeddingService.model.encode(
#                 ["Instruct: Retrieve relevant document passages\nQuery: " + q
#                 for q in texts],
#                 normalize_embeddings=True,
#             )
#         )

##################################################################################

from sentence_transformers import (SentenceTransformer,)
from app.core.config import settings
from app.schemas.parser import (Chunk,)

class EmbeddingService:

    MODEL_NAME = (settings.EMBEDDING_MODEL_NAME)

    DOCUMENT_PREFIX = ("Represent this sentence for retrieval: ")

    QUERY_PREFIX = ("Represent this question for searching relevant passages: ")

    model = SentenceTransformer(MODEL_NAME, local_files_only=True)

    @staticmethod
    def embed_documents(texts: list[str],) -> list[list[float]]:

        prefixed_texts = [
            (EmbeddingService.DOCUMENT_PREFIX + text)for text in texts]

        embeddings = (
            EmbeddingService.model.encode(
                prefixed_texts,normalize_embeddings=True,convert_to_numpy=True,
                ))

        return embeddings.tolist()

    @staticmethod
    def embed_query(query: str,) -> list[float]:

        prefixed_query = (EmbeddingService.QUERY_PREFIX+ query)

        embedding = (
            EmbeddingService.model.encode(
                prefixed_query,normalize_embeddings=True,convert_to_numpy=True,
                ))

        return embedding.tolist()
    
    @staticmethod
    def embed_chunks(chunks: list[Chunk],):

        texts = [chunk.text for chunk in chunks]

        embeddings = (
            EmbeddingService.embed_documents(texts))

        chunk_embeddings = []

        for chunk, embedding in zip(chunks,embeddings,):

            chunk_embeddings.append(
                {
                    "chunk": chunk,
                    "embedding": embedding,
                }
            )

        return chunk_embeddings