import logging
import requests
from time import sleep
import datetime
import settings
import random

LOG_HTTP_CALL = False


def log_http_call():
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def url(query, next_token):
    expansions = 'tweet.fields=created_at,public_metrics,lang&expansions=author_id&user.fields=created_at'
    options = " -is:retweet (lang:it OR lang:en)"
    query += options
    max_results_string = 'max_results=100'
    start_time_string = f"start_time={oldest_timestamp()}"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&{expansions}&{max_results_string}&{start_time_string}"
    if next_token:
        url += f"&next_token={next_token}"
    return url

def oldest_timestamp():
    f = open(settings.TIMESTAMP_FILE, 'r')
    return f.read().strip()


def response(query, next_token=None):
    api_url = url(query, next_token)
    headers = {"Authorization": f"Bearer {random.choice(settings.BEARER_TOKENS)}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 429:
        reset_time = datetime.datetime.fromtimestamp(int(response.headers['x-rate-limit-reset'])) + datetime.timedelta(seconds=30)
        print(f"sleep until {reset_time}")
        sleep((reset_time - datetime.datetime.now()).seconds)
        return {'error': 'rate limit'}
    if response.status_code != 200:
        print(f"{response.status_code} - {response.text}")
        return {'error': 'general error'}
    return response.json()


if LOG_HTTP_CALL:
    log_http_call()
