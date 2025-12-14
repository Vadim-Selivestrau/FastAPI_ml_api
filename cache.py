import redis
import hashlib
import json
import os
from loger import logger

REDIS_HOST = os.getenv("REDIS_HOST", "localhost") 
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379)) 
 
redis_client = redis.Redis( 
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=0 
)

def get_from_cache(key: str):
    hash_key = hashlib.sha256(key.encode()).hexdigest()
    json_value = redis_client.get(hash_key)
    
    if json_value is None:
        logger.info("❌ Cache miss for key=%s", key)
        return None

    try:
        value = json.loads(json_value)
    except json.JSONDecodeError:
        logger.error("❌ Failed to decode JSON for key=%s", key)
        return None

    logger.info("✔ Cache hit for key=%s", key)
    return value  


def set_to_cache(key: str, value):
    hash_key = hashlib.sha256(key.encode()).hexdigest()
    json_value = json.dumps(value)
    redis_client.set(hash_key, json_value, ex=900)
