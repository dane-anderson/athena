"""
Athena Memory Retrieval

Searches Athena's semantic memory using
Kev embeddings + ChromaDB.

Supports optional memory scopes so agents
can retrieve the most relevant knowledge.
"""

from memory.memory_store import search_memory


def retrieve(
    query,
    limit=5,
    scope=None,
):
    """
    Return the most relevant stored memories.

    scope examples:
        mathematics
        computer_science
        research
        security
        conversations
        machine_learning

    If scope is None, search all memory.
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


        # Filter by memory scope when requested
        if scope:

            memory_scope = metadata.get(
                "scope",
                metadata.get(
                    "collection",
                    None,
                ),
            )

            if memory_scope != scope:
                continue


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