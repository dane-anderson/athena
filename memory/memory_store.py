"""
Athena Memory Store

Persistent semantic memory using:
- Qwen3 Embedding through Ollama
- ChromaDB for local vector storage
"""

from pathlib import Path
import time

import chromadb
import requests


OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "kev"

MEMORY_PATH = Path(__file__).parent / "vector_store"

client = chromadb.PersistentClient(
    path=str(MEMORY_PATH)
)

collection = client.get_or_create_collection(
    name="athena_memory"
)


def embed_text(text: str):
    """
    Generate an embedding using Athena's
    local Kev embedding model.
    """

    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": text,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()["embeddings"][0]


def store_memory(
    memory_id: str,
    text: str,
    metadata=None,
    scope=None,
):
    """
    Store text and its embedding in Athena memory.
    """

    if metadata is None:
        metadata = {}

    if scope:
        metadata["scope"] = scope

    embedding = embed_text(text)

    collection.upsert(
        ids=[memory_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata],
    )
    """
    Store text and its embedding in Athena memory.
    """

    if metadata is None:
        metadata = {}

    embedding = embed_text(text)

    collection.upsert(
        ids=[memory_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata],
    )


def search_memory(
    query: str,
    limit=5,
    scope=None,
):
    """
    Retrieve semantically similar memories.

    If a scope is provided, Chroma searches only
    memories belonging to that scope.
    """

    query_embedding = embed_text(query)

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": limit,
    }

    if scope:
        query_args["where"] = {
            "scope": scope
        }

    return collection.query(
        **query_args
    )


if __name__ == "__main__":
    store_memory(
        memory_id="test_memory",
        text="Athena is a local multi-agent AI system.",
        metadata={
            "type": "test"
        },
    )

    results = search_memory(
        "What kind of AI system is Athena?"
    )

    print(results)