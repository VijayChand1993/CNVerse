import json

from app.core.queue import INGESTION_QUEUE
from app.core.redis import redis_client

class QueueService:

    @staticmethod
    def enqueue_ingestion_job(payload : dict):
        redis_client.lpush(INGESTION_QUEUE, json.dumps(payload))