import os
import csv
import json
from sentiment_analysis.run import analyze
import datetime

TWEET_TYPES = ['hashtag_company', 'account']
COMPANIES_TWEET_FILE = ['apple', 'amazon', 'facebook', 'netflix']
ACCOUNT_TWEET_FILE = ['Apple', 'AmazonNewsItaly', 'Facebook', 'NetflixIT']


def is_skipped_tweet_file(filename):
    name = filename.split('.')[0]
    return name in COMPANIES_TWEET_FILE or name in ACCOUNT_TWEET_FILE


def parse_date(row_date):
    date, hour = row_date.split('T')
    splitted_time = hour.split(':')
    return f"{date} {splitted_time[0]}:{splitted_time[1]}"


def create_directory(date):
    directory_path = f"/home/marco/Scrivania/tirocinio-unicredit/graphdb/nodes/{date}/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def oldest_timestamp():
    f = open('/home/marco/Scrivania/tirocinio-unicredit/graphdb/timestamp.txt', 'r')
    return f.read().strip()


def nodes_file():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    c = 0
    create_directory(today)
    with open(f"/home/marco/Scrivania/tirocinio-unicredit/graphdb/nodes/{today}/tweet_nodes.csv", mode='w') as nodes_file:
        timestamp = oldest_timestamp()
        fieldnames = ['id', 'text', 'sentiment_score', 'date']
        writer = csv.DictWriter(nodes_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for type in TWEET_TYPES:
            for dir in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/"):
                if dir <= timestamp:
                    continue

                for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/{dir}/"):
                    if is_skipped_tweet_file(filename):
                        continue

                    file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/{dir}/" + filename)
                    parsed_file = json.load(file)
                    for tweet in parsed_file['data']:
                        print(c)
                        c += 1
                        writer.writerow(
                            {
                                'id': tweet['id'],
                                'text': tweet['text'].replace('|', ' '),
                                'sentiment_score': analyze(tweet['text']),
                                'date': parse_date(tweet['created_at'])
                            }
                        )
