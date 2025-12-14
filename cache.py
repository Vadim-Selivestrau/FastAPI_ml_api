import redis
import hashlib
from loger import logger

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0
)
redis_client.expire

if redis_client.ping():
    pass#redis IS WORK
else:
    print("redis doesnt work")


def get_from_cache(key: str):
    '''
    что можно улучшить. Добавить обработу запросов, например
    приводить всё к единому регистру, убирать ненужные символы
    '''
    hash_object = hashlib.sha256(key.encode())
    hash_key = hash_object.hexdigest()
    value = redis_client.get(hash_key)
    if value is None:    
        logger.info("❌Cache miss for key=%s", key)
        return None
    logger.info("✔Cache hit for key=%s", key)
    return value.decode("utf-8")



def set_to_cache(key: str, value: str):
    hash_object = hashlib.sha256(key.encode())
    hash_key = hash_object.hexdigest()
    redis_client.set(hash_key, value, ex=900)
