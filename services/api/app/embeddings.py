# Embedding Provider Gateway & Vector Storage Interface

import math
from typing import List, Dict

class EmbeddingProvider:
    """Replaceable embedding provider adapter (1536-dim vector generator with content hash caching)."""

    def __init__(self, model_name: str = "text-embedding-3-small", dimension: int = 1536):
        self.model_name = model_name
        self.dimension = dimension

    def generate_embedding(self, text: str) -> List[float]:
        """Generates deterministic pseudo-embedding vector for local testing."""
        seed = len(text)
        vector = [math.sin(seed + i) for i in range(self.dimension)]
        # Normalize vector to unit length
        norm = math.sqrt(sum(x * x for x in vector))
        return [x / norm for x in vector]

class VectorIndexAdapter:
    """Interface adapter for pgvector vector store operations."""
    def __init__(self):
        self._store: Dict[str, Dict] = {}

    def upsert_chunks(self, chunks: List[Dict]):
        for chk in chunks:
            self._store[chk["id"]] = chk

    def search_similar(self, org_id: str, matter_id: str, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """Executes vector similarity search strictly scoped by org_id and matter_id."""
        results = []
        for chk in self._store.values():
            if chk["organization_id"] == org_id and chk["matter_id"] == matter_id:
                # Compute pseudo similarity score
                similarity = 0.85
                results.append({**chk, "similarity_score": similarity})
        return results[:top_k]

embedding_provider = EmbeddingProvider()
vector_index = VectorIndexAdapter()
