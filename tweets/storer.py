import tweets.endpoint as endpoint
import tweets.filter as filter
import json
import os
from datetime import date
import settings


def store(informations, kind):
    print(f"===== {kind.upper()} =====")
    for information in informations:
        query = twitter_query(information, kind)
        json_response = endpoint.response(query)
        if is_incompleted_response(json_response):
            json_response = fill_response(json_response, query, information)

        if json_response.get('error') == 'rate limit':
            json_response = endpoint.response(query)

        if json_response.get('error') == 'general error':
            continue

        filter.filter(json_response)

        if json_response['meta']['result_count'] == 0:
            print(f"skip {information} because 0 tweet")
            continue

        unique_author(json_response)
        save_response(json_response, information, kind)
        print(f"wrote {json_response['meta']['result_count']} tweets of {information}")


def is_incompleted_response(json_response):
    token = json_response.get('meta') and json_response['meta'].get('next_token')
    return not(not(token))


def fill_response(json_response, query, information):
    next_token = json_response['meta'].get('next_token')
    while next_token:
        next_response = endpoint.response(query, next_token)
        if next_response.get('error') == 'rate limit':
            next_response = endpoint.response(query, next_token)
        print(f"find more {next_response['meta']['result_count']} tweet of {information}")
        json_response['data'] += next_response['data']
        json_response['includes']['users'] += next_response['includes']['users']
        json_response['meta']['oldest_id'] = next_response['meta']['oldest_id']
        next_token = next_response['meta'].get('next_token')
    return json_response


def twitter_query(information, kind):
    if kind == 'hashtag_ticker' or kind == 'hashtag_company' or kind == 'index':
        q = f"%23{information}"
    else:
        q = f"from: {information}"
    return q


def save_response(json_response, information, kind):
    today = date.today()
    directory_path = settings.TWEETS_DATA_FOLDER + f"{kind}/{today}/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    with open(settings.TWEETS_DATA_FOLDER + f"{kind}/{today}/{information}.json", 'w') as outfile:
        json.dump(json_response, outfile)


def unique_author(json_response):
    ids = set(map(lambda d: d['author_id'], json_response['data']))
    authors = []
    for user in json_response['includes']['users']:
        if user['id'] in ids:
            ids.remove(user['id'])
            authors.append(user)
    json_response['includes']['users'] = authors
