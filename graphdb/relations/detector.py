def language(tweet, nlp_detect):
    lang = tweet.get('lang')
    if lang:
        return lang
    return detect_language(tweet, nlp_detect)


def detect_language(tweet, nlp_detect):
    try:
        doc = nlp_detect(tweet['text'])
        return doc._.languages[0]
    except Exception as e:
        print(e)
        return None
