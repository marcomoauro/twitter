import os
import json
import quotes.utils as utils


def load_tweets(date):
    tweets = []
    for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag/{date}/"):
        file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag/{date}/" + filename)
        parsed_file = json.load(file)
        tweets += parsed_file['data']
    return tweets


def find(date):
    tweets = load_tweets(date)
    tweets_quotes = []
    names, accounts = utils.data()
    for tweet in tweets:
        text = tweet['text']
        quotes = utils.companies_quotes(text, accounts)
        if len(quotes) < 2:
            continue
        tweets_quotes.append({'text': text, 'companies': quotes})
    if len(tweets_quotes) > 0:
        utils.save_data(tweets_quotes, 'hashtag', date)
    return tweets_quotes
