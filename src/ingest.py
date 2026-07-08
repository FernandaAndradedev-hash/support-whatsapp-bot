"""
Indexa a base de conhecimento da VendaMais no Qdrant.
"""
import hashlib
import logging
import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

import config
from knowledge_base import get_all_documents, get_full_text

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

_openai = OpenAI(api_key=config.OPENAI_API_KEY)
_qdrant = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)


def _ensure_collection():
    existing = {c.name for c in _qdrant.get_collections().collections}
    if config.QDRANT_COLLECTION not in existing:
        _qdrant.create_collection(
            collection_name=config.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=config.EMBEDDING_DIMENSIONS,
                distance=Distance.COSINE,
            ),
        )
        logger.info("Coleção '%s' criada.", config.QDRANT_COLLECTION)


def ingest_all():
    _ensure_collection()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    total = 0

    for doc in get_all_documents():
        full_text = get_full_text(doc)
        doc_hash = hashlib.sha256(full_text.encode()).hexdigest()

        results, _ = _qdrant.scroll(
            collection_name=config.QDRANT_COLLECTION,
            scroll_filter={"must": [{"key": "doc_hash", "match": {"value": doc_hash}}]},
            limit=1, with_payload=False, with_vectors=False,
        )
        if results:
            logger.info("Já indexado: '%s'. Pulando.", doc["title"])
            continue

        chunks = splitter.split_text(full_text)
        response = _openai.embeddings.create(model=config.EMBEDDING_MODEL, input=chunks)
        embeddings = [item.embedding for item in response.data]

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={
                    "text": chunk,
                    "title": doc["title"],
                    "category": doc["category"],
                    "doc_hash": doc_hash,
                },
            )
            for chunk, emb in zip(chunks, embeddings)
        ]

        _qdrant.upsert(collection_name=config.QDRANT_COLLECTION, points=points, wait=True)
        total += len(points)
        logger.info("Indexado: '%s' (%d chunks)", doc["title"], len(points))

    logger.info("Ingestão concluída. Total: %d chunks", total)


if __name__ == "__main__":
    ingest_all()