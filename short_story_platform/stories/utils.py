import redis
import json

rd = redis.StrictRedis(host='localhost', port=6379, db=0)


class RedisHandler:
    @staticmethod
    def set_code(cache_key, code, expiry=3600):
        rd.set(cache_key, json.dumps(code), ex=expiry)
        return True

    @staticmethod
    def get_code(cache_key):
        code_data = rd.get(cache_key)
        if not code_data:
            return None
        return json.loads(code_data)
