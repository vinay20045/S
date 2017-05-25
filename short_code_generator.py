import itertools
import math
import config

import redis
rdb = redis.StrictRedis(
        host = config.redis['host'], 
        port = config.redis['port'], 
        db = config.redis['db']
    )

def populate_short_code(pos, n, r):
    if r > config.code_generator['r_max']:
        return
    if pos < math.pow(n,r):
        for tup in itertools.product(config.code_generator['char_set'], repeat=r):
            key = config.code_generator['escape_prefix'] + str(pos)
            val = ''.join(tup)
            if val not in config.blocked_short_codes:
                if rdb.set(key, val):
                    pos = pos + 1
                    # print key, val
        populate_short_code(pos, n, r+1)

if __name__ == '__main__':
    n = len(config.code_generator['char_set'])
    r = config.code_generator['r_min']
    populate_short_code(1, n, r)