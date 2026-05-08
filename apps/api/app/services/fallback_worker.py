import threading
import time

from app.core.memory_queue import (
    memory_ingestion_queue,
)


def process_payload(payload: dict):

    print(
        f"[Fallback Worker] "
        f"Processing payload: {payload}"
    )

    time.sleep(2)

    print("[Fallback Worker] Done")


def fallback_worker_loop():

    print("Fallback worker started")

    while True:

        if not memory_ingestion_queue.empty():

            payload = (
                memory_ingestion_queue.get()
            )

            try:
                process_payload(payload)

            except Exception as exc:
                print(
                    f"[Fallback Worker] "
                    f"Failed: {exc}"
                )

        time.sleep(1)


def start_fallback_worker():

    thread = threading.Thread(
        target=fallback_worker_loop,
        daemon=True,
    )

    thread.start()