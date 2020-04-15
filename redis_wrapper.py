import redis
REDIS_SERVER_CONF = {
  'HOST': 'localhost',
  'PORT': 6379,
  'DATABASE': 0
}


class RedisWrapper(object):
    shared_state = {}

    def __init__(self):
        self.__dict__ = self.shared_state

    def redis_connect(self):
        redis_server_conf = REDIS_SERVER_CONF
        connection_pool = redis.ConnectionPool(host=redis_server_conf['HOST'], port=redis_server_conf['PORT'],
                                               db = redis_server_conf['DATABASE'])
        return redis.StrictRedis(connection_pool = connection_pool)
