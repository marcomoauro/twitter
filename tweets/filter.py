def filter_for_reply(response):
    filtered_data = []
    for tweet in response['data']:
        if is_reply(tweet):
            continue

        filtered_data.append(tweet)
    response['data'] = filtered_data
    response['meta']['result_count'] = len(filtered_data)

def is_reply(tweet):
    return tweet['text'][0] == '@'
