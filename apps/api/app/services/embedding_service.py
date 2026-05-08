from sentence_transformers import SentenceTransformer

class EmbeddingService:
    model = SentenceTransformer("storage/models/Qwen3-Embedding-0.6B", local_files_only=True)

    @staticmethod
    def embed_texts(
        texts: list[str],
    ):
        # For embedding queries — instruction improves retrieval 1-5%
        return (
            EmbeddingService.model.encode(
                ["Instruct: Retrieve relevant document passages\nQuery: " + q
                for q in texts],
                normalize_embeddings=True,
            )
        )