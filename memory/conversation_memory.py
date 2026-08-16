"""
Athena Conversation Memory

Stores useful conversation turns in Athena's
semantic memory using Kev + ChromaDB.
"""

from datetime import datetime
import hashlib

from memory.memory_store import store_memory


def save_conversation(
    user_message: str,
    assistant_response: str,
    topic: str = "general",
    importance: str = "normal",
):
    """
    Store one conversation turn in long-term memory.
    """

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    text = f"""
User:
{user_message}

Athena:
{assistant_response}
""".strip()


    memory_id = hashlib.sha256(
        (
            timestamp
            + user_message
            + assistant_response
        ).encode()
    ).hexdigest()


    metadata = {
        "type": "conversation",
        "scope": "conversations",
        "topic": topic,
        "importance": importance,
        "timestamp": timestamp,
    }


    store_memory(
        memory_id=memory_id,
        text=text,
        metadata=metadata,
        scope="conversations",
    )


    return memory_id



if __name__ == "__main__":

    memory_id = save_conversation(
        user_message=(
            "I want Athena to remember "
            "conversations."
        ),
        assistant_response=(
            "Conversation memory is "
            "being improved."
        ),
        topic="athena_memory",
        importance="high",
    )

    print(
        f"Saved conversation memory: {memory_id}"
    )