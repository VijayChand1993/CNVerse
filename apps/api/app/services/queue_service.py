import json

from redis.exceptions import RedisError

from app.core.memory_queue import (
    memory_ingestion_queue,
)
from app.core.queue import INGESTION_QUEUE
from app.core.redis import redis_client


class QueueService:

    @staticmethod
    def enqueue_ingestion_job(
        payload: dict,
    ):

        try:
            redis_client.lpush(
                INGESTION_QUEUE,
                json.dumps(payload),
            )

            print("Job queued in Redis")

        except RedisError:

            memory_ingestion_queue.put(payload)

            print(
                "Redis unavailable. "
                "Job queued in memory queue."
            )