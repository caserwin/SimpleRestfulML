# coding=utf-8
import redis
import json
from src.utils import config


class RedisClient(object):
    config_key = 'redis'

    def __init__(self):
        self.host = config.get(self.config_key, 'host')
        self.port = config.get(self.config_key, 'port')
        self.db = config.get(self.config_key, 'db')
        self.redis_client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def delete_key(self, keystr):
        key_list = []
        for key in self.redis_client.scan_iter(match=keystr + '*', count=10000):
            key_list.append(key)

        for key in key_list:
            self.redis_client.delete(key)

    def set_cache_data(self, contents, expire=3600 * 24):
        for content in contents:
            key = content['key']
            content.pop('key')
            self.redis_client.setex(key, expire, json.dumps(content))

    def get_cache_data(self, key):
        keys = self.redis_client.keys(key + "*")
        pipe = self.redis_client.pipeline()
        for key in keys:
            pipe.get(key)

        res_ls = []
        for (k, v) in zip(keys, pipe.execute()):
            res_ls.append(v)
        return res_ls
