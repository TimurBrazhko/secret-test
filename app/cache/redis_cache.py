import redis
import json
from app.core.config import settings
from datetime import timedelta


def get_redis_client():
    return redis.StrictRedis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        decode_responses=True
    )


def cache_secret(secret_key: str, secret: str, ttl_seconds: int):
    redis_client = get_redis_client()

    secret_data = json.dumps({"secret": secret})

    redis_client.setex(secret_key, timedelta(seconds=ttl_seconds), secret_data)


def get_cached_secret(secret_key: str):
    redis_client = get_redis_client()

    secret_data = redis_client.get(secret_key)

    if secret_data:
        return json.loads(secret_data).get("secret")
    return None


def delete_cached_secret(secret_key: str):
    redis_client = get_redis_client()

    redis_client.delete(secret_key)
