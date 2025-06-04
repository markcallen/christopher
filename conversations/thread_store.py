from datetime import datetime

threads: dict[str, list[dict]] = {}


def save_message(thread_id: str, sender: str, content: str):
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
    return threads.get(thread_id, [])


def list_threads() -> list[str]:
    return list(threads.keys())
