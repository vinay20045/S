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

redis = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}

long_url_length = 2000

short_url_domain = 'http://your.domain/'    # Has to have trailing /

code_generator = {
    "char_set": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_",
    "escape_prefix": "$",   # Ensure that this character is not part of the char_set
    "r_min": 1,
    "r_max": 3
}

# Basically, these are the words which are...
# 1. Reserved (like get) and you have some other use for them
# 2. Cuss words you probably wouldn't want the urls to contain
# Add as many as you want, it will filter them out during generation.
blocked_short_codes = [
    'get',
    'satan',
    's3x'
]