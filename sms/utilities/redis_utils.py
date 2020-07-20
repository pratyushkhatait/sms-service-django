import redis
import time
import logging
from ast import literal_eval
from sms.config import REDIS, DEFAULT_TTL
logger = logging.getLogger(__name__)


class RedisUtil:
    """
    This class is used to create redis connection,
    set key-val pairs
    get val for a given key
    increment a count of a key
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.count = 0
        self.max_retry = 5
        try:
            self._redis = redis.Redis(host=self.host, port=self.port, db=0)
        except redis.ConnectionError as err:
            self.count += 1
            if self.count > self.max_retry:
                logger.error("RedisUtil: Redis connection error: max retry={} reached".format(self.max_retry))
            else:
                # wait for 5 seconds
                time.sleep(5)
                logger.info("RedisUtil: Retrying in 5 seconds")
                self._redis = redis.Redis(host=self.host, port=self.port, db=0)
        logger.info("RedisUtil: Successfully established connection with redis: host={}, port={}"
                    .format(self.host, self.port))

    def get_redis_object(self, key):
        try:
            obj = self._redis.get(key)
            if obj:
                obj = literal_eval(obj.decode("utf-8"))
            return obj
        except Exception as err:
            logger.error("RedisUtil: Get Redis object error:: {} : key:{}".format(str(err), key))
            return

    def set_redis_object(self, key, val, expiry=DEFAULT_TTL):
        try:
            self._redis.set(key, val, ex=expiry)
        except Exception as err:
            logger.error("RedisUtil: Set Redis object error:: {} : key:{} val:{}".format(str(err), key, val))

    def increment_redis_object(self, key, delta=1):
        try:
            res = self.get_redis_object(key)
            if res:
                self.set_redis_object(key, res+delta)
            else:
                self.set_redis_object(key, 1)
        except Exception as err:
            self.set_redis_object(key, 1)


# Create a Redis object
redis = RedisUtil(REDIS["host"], REDIS["port"])
