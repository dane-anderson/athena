"""
Athena Memory Retrieval

Searches Athena's semantic memory using
Kev embeddings + ChromaDB.
"""

from memory.memory_store import search_memory


def retrieve(query, limit=5):
    """
    Return the most relevant stored memories
    for a query.
    """

    results = search_memory(
        query=query,
        limit=limit,
    )

    documents = (
        results.get("documents", [[]])[0]
    )

    metadatas = (
        results.get("metadatas", [[]])[0]
    )

    distances = (
        results.get("distances", [[]])[0]
    )

    memories = []

    for index, document in enumerate(documents):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        memories.append(
            {
                "content": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return memories


if __name__ == "__main__":

    results = retrieve(
        "What kind of AI system is Athena?"
    )

    for result in results:
        print(result)