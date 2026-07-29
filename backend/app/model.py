# Right now main.py is not using this file, instead main.py has its seperate code for this in itself.

from typing import Sequence, List, Tuple, Union
import torch
from sentence_transformers import SentenceTransformer, util


class EmbeddingHelper:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = None):
        # pick a device if not provided
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model = SentenceTransformer(model_name, device=self.device)

    def embed_list(self, texts: Sequence[str]):
        if not texts:
            return torch.empty((0, self.model.get_sentence_embedding_dimension()), device=self.device)
        return self.model.encode(list(texts), convert_to_tensor=True, device=self.device)

    def query_top(self, query: str, corpus_embeddings: Union[torch.Tensor, Sequence[Sequence[float]]], top_k: int = 1) -> List[Tuple[int, float]]:
        if not query:
            return []

        # encode query
        q_emb = self.model.encode(query, convert_to_tensor=True, device=self.device)

        # ensure corpus_embeddings is a tensor on the same device
        if not torch.is_tensor(corpus_embeddings):
            corpus_embeddings = torch.tensor(corpus_embeddings, device=self.device)

        corpus_embeddings = corpus_embeddings.to(self.device)

        if corpus_embeddings.numel() == 0:
            return []

        # normalize for cosine similarity (recommended)
        q_emb = util.normalize_embeddings(q_emb)
        corpus_embeddings = util.normalize_embeddings(corpus_embeddings)

        hits = util.semantic_search(q_emb, corpus_embeddings, top_k=top_k)[0]
        return [(h["corpus_id"], float(h["score"])) for h in hits]
