import redis
from secret_keys import SecretKeys

secret_keys = SecretKeys()

# redis_client = redis.Redis(host="redis", port=6379,)

redis_client = redis.Redis(
    host=secret_keys.REDIS_DB_HOST,
    port=secret_keys.REDIS_DB_PORT,
    username="default",
    password=secret_keys.REDIS_DB_PASSWORD,
    decode_responses=True,
)
