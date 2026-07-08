"""
Busca semântica na base de conhecimento da VendaMais.
"""
import logging

from openai import OpenAI
from qdrant_client import QdrantClient

import config

logger = logging.getLogger(__name__)

_openai = OpenAI(api_key=config.OPENAI_API_KEY)
_qdrant = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)


def retrieve(query: str, category: str | None = None) -> list[dict]:
    """
    Busca chunks relevantes para a pergunta do cliente.

    Args:
        query: Pergunta do cliente (sanitizada).
        category: Filtro opcional por categoria.

    Returns:
        Lista de chunks com text, title, category e score.
    """
    response = _openai.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=query,
    )
    query_vector = response.data[0].embedding

    search_filter = None
    if category:
        search_filter = {
            "must": [{"key": "category", "match": {"value": category}}]
        }

    results = _qdrant.search(
        collection_name=config.QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=config.RETRIEVAL_TOP_K,
        with_payload=True,
        score_threshold=config.MIN_SCORE_THRESHOLD,
        query_filter=search_filter,
    )

    return [
        {
            "text": hit.payload["text"],
            "title": hit.payload.get("title", ""),
            "category": hit.payload.get("category", ""),
            "score": round(hit.score, 4),
        }
        for hit in results
    ]