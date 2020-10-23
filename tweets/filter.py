import tweets.constants as constants


def filter(response):
    filtered_data = []
    for tweet in response.get('data', []):
        if is_reply(tweet):
            continue
        if not contain_keywords(tweet):
            continue

        filtered_data.append(tweet)
    response['data'] = filtered_data
    response['meta']['result_count'] = len(filtered_data)


def is_reply(tweet):
    return tweet['text'][0] == '@'


def contain_keywords(tweet):
    for keyword in constants.FINANCE_KEYWORDS:
        words = tweet['text'].lower().split(' ')
        for word in words:
            if keyword == word:
                return True
    return False
