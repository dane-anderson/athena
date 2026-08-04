"""
Athena Research Librarian

Finds relevant knowledge from Athena's
research library.
"""

from pathlib import Path


LIBRARY_PATH = Path(
    "memory/research_library"
)



def load_documents():

    documents = []

    for file in LIBRARY_PATH.rglob("*.md"):

        content = file.read_text(
            encoding="utf-8"
        )

        documents.append(
            {
                "file": str(file),
                "content": content
            }
        )

    return documents



def retrieve(query, limit=3):

    """
    Simple keyword retrieval.

    Later this becomes embedding retrieval
    using qwen3-embedding.
    """

    query_words = (
        query.lower()
        .split()
    )


    results = []


    for document in load_documents():

        score = 0

        text = (
            document["content"]
            .lower()
        )


        for word in query_words:

            if word in text:
                score += 1


        if score > 0:

            results.append(
                (
                    score,
                    document
                )
            )


    results.sort(
        key=lambda x: x[0],
        reverse=True
    )


    return [
        document
        for score, document
        in results[:limit]
    ]