##
# This is as simple as a license can get. Please read 
# carefully and understand before using.
#
# I wrote this script because I needed it. I am opening
# up the source code to the world because I believe in 
# the power of royalty free knowledge and shared ideas.
#
# 1. This piece of code comes to you at no cost and no 
#    obligations.
# 2. You get NO WARRANTIES OR GUARANTEES OR PROMISES of
#    any kind.
# 3. If you are using this script you understand the risks
#    completely.
# 4. I request and insist that you retain this notice without
#    modification, but if you can't... I understand.
#
# --
# Vinay Kumar NP 
# vinay@askvinay.com
# www.askVinay.com
##

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