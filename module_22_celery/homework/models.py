import redis
from config import CELERY_BROKER_URL

redis_client = redis.Redis.from_url(CELERY_BROKER_URL, decode_responses=True)

def subscribe(email: str) -> bool:
    return redis_client.sadd('subscribers', email) > 0

def unsubscribe(email: str) -> bool:
    return redis_client.srem('subscribers', email) > 0

def get_all_subscribers() -> list:
    return list(redis_client.smembers('subscribers'))