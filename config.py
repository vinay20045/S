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