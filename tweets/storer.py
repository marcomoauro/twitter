import tweets.endpoint as endpoint
import json
import os
from datetime import date


def store(informations, type):
    print(f"===== {type.upper()} =====")
    today = date.today()
    for information in informations:
        query = twitter_query(information, type)
        json_response = endpoint.response(query)
        next_token = json_response['meta'].get('next_token')
        while next_token:
            next_response = endpoint.response(query, next_token)
            print(f"find more {next_response['meta']['result_count']} tweet of {information}")
            json_response['data'] += next_response['data']
            json_response['includes']['users'] += next_response['includes']['users']
            json_response['meta']['result_count'] += next_response['meta']['result_count']
            json_response['meta']['oldest_id'] = next_response['meta']['oldest_id']
            next_token = next_response['meta'].get('next_token')

        if json_response.get('error') == 'rate limit':
            json_response = endpoint.response(query)

        if json_response.get('error') == 'general error':
            continue

        result_count = json_response['meta']['result_count']
        if result_count == 0:
            print(f"skip {information} because 0 tweet")
            continue

        directory_path = f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/{str(today)}/"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        with open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/{str(today)}/{information}.json",
                  'w') as outfile:
            json.dump(json_response, outfile)
            print(f"wrote {result_count} tweets of {information}")


def twitter_query(information, type):
    if type == 'hashtag':
        q = f"%23{information}"
    else:
        q = f"from: {information}"
    return q
