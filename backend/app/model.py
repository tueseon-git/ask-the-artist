# Optional wrapper if you want to isolate embedding logic here
from sentence_transformers import SentenceTransformer, util


class EmbeddingHelper:
def __init__(self, model_name='all-MiniLM-L6-v2'):
self.model = SentenceTransformer(model_name)


def embed_list(self, texts):
return self.model.encode(texts, convert_to_tensor=True)


def query_top(self, query, corpus_embeddings, top_k=1):
q_emb = self.model.encode(query, convert_to_tensor=True)
return util.semantic_search(q_emb, corpus_embeddings, top_k=top_k)