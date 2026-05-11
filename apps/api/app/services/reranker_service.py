import torch

from transformers import (AutoModelForSequenceClassification,AutoTokenizer,)


class RerankerService:

    MODEL_NAME = ("storage/models/bge-reranker-v2-m3")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)

    model = (AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, local_files_only=True))

    model.eval()

    @staticmethod
    def rerank(query: str, results: list, top_k: int = 5,):

        if not results:
            return []
        
        pairs = []
        for result in results:
            text = (result["_source"]["text"])

            pairs.append([query, text])

        with torch.no_grad():
            inputs = (
                RerankerService.tokenizer(
                    pairs,
                    padding=True,
                    truncation=True,
                    return_tensors="pt",
                    max_length=1024,
                )
            )

            scores = (
                RerankerService.model(
                    **inputs,
                    return_dict=True,
                )
                .logits
                .view(-1,)
                .float()
            )

        reranked_results = []

        for result, score in zip(results, scores.tolist(),):
            result["rerank_score"] = score
            result["original_score"] = (result["_score"])
            
            reranked_results.append(
                result
            )

        reranked_results.sort(key=lambda x: (x["rerank_score"]), reverse=True,)

        return reranked_results[:top_k]