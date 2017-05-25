# Load flask
import flask
from flask import Flask
app = Flask(__name__)

import config
import urllib
import json

# Load redis
import redis
r = redis.StrictRedis(
        host = config.redis['host'], 
        port = config.redis['port'], 
        db = config.redis['db']
    )

# App routes -- These strings follow flask route construction rules
route_redirect_request = '/<url_key>'
route_get_short_url = '/get' 

@app.route(route_redirect_request)
def redirect_request(url_key):
    if not r.get(url_key):
        flask.abort(404)
    else:
        return flask.redirect(urllib.unquote(r.get(url_key)), code=301)

@app.route(route_get_short_url, methods=['POST'])
def get_short_url():
    long_url = flask.request.form.get('url')
    if not long_url:
        return json.dumps(['failure', 'No url sent'])
    else:
        try:
            # Check URL validity
            if len(long_url) > config.long_url_length:
                return json.dumps(['failure', 'Url length not accepted'])
            res = urllib.urlopen(long_url)
            if res.getcode() not in (200, 301, 302):
                return json.dumps(['failure', 'Url does not seem to be valid'])

            # Check URL existence and return short_code
            encoded_url = urllib.quote_plus(long_url, safe='/')
            url_key = r.get(encoded_url)
            if not url_key:
                url_key = r.get(config.code_generator['escape_prefix'] + str(r.incr('counter')))
                r.set(url_key, encoded_url)
                # Exploiting redis for faster lookups :)
                r.set(encoded_url, url_key)
            return json.dumps(['success', config.short_url_domain + url_key])
        except:
            return json.dumps(['failure', 'Some error occured'])

if __name__ == '__main__':
    app.run(debug=False)