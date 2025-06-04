"""Thread store for storing and retrieving conversation threads."""

from datetime import datetime

threads: dict[str, list[dict]] = {}


def save_message(thread_id: str, sender: str, content: str):
    """Save a message to the thread store."""
    if thread_id not in threads:
        threads[thread_id] = []
    threads[thread_id].append(
        {
            "sender": sender,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )


def get_thread(thread_id: str) -> list[dict]:
    """Get a thread from the thread store."""
    return threads.get(thread_id, [])


def list_threads() -> list[str]:
    """List all threads in the thread store."""
    return list(threads.keys())
