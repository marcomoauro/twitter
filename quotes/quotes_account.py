import os
import json
import quotes.utils as utils


def load_tweets(date):
    tweets = []
    for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/account/{date}/"):
        file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/account/{date}/" + filename)
        parsed_file = json.load(file)
        for tweet_data in parsed_file['data']:
            tweet_data['pub_account'] = filename.split('.')[0]
        tweets += parsed_file['data']
    return tweets


def find(date):
    tweets = load_tweets(date)
    tweets_quotes = []
    names, accounts = utils.data()
    for tweet in tweets:
        text = tweet['text']
        quotes = utils.companies_quotes(text, accounts)
        if tweet['pub_account'] in quotes:
            quotes.remove(tweet['pub_account'])
        if len(quotes) < 1:
            continue
        tweets_quotes.append({'text': text, 'companies': quotes, 'publisher': tweet['pub_account']})
    if len(tweets_quotes) > 0:
        utils.save_data(tweets_quotes, 'account', date)
    return tweets_quotes
