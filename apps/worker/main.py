import json
import time

from redis_client import redis_client

QUEUE_NAME = "ingestion_queue"

def process_job(payload: dict):
    print(f"Processing job : {payload}")
    time.sleep(2)
    print("Job completed")

def main():
    print("Worker started...")

    while True:
        _, message = redis_client.brpop(QUEUE_NAME)

        payload = json.loads(message)

        try:
            process_job(payload)

        except Exception as exc:

            retry_count = payload.get(
                "retry_count",
                0,
            )

            print(f"Job failed: {exc}")

            if retry_count < 3:

                payload["retry_count"] = (
                    retry_count + 1
                )

                redis_client.lpush(
                    QUEUE_NAME,
                    json.dumps(payload),
                )

                print(
                    f"Retrying job "
                    f"({payload['retry_count']}/3)"
                )

            else:
                print("Job permanently failed")


if __name__ == "__main__":
    main()
