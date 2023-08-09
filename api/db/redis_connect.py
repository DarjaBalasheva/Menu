import os

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get('redis_host')
REDIS_PORT = os.environ.get('redis_port')
REDIS_DB = os.environ.get('redis_db')


def connect_to_redis():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
