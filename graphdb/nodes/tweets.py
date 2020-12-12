import os
import csv
import json
from sentiment_analysis.run import analyze
import datetime
import settings
from graphdb.utils import name_parser

TWEET_TYPES = ['account', 'hashtag_company']
COMPANIES_TWEET_FILE = ['apple', 'amazon', 'facebook', 'netflix']
ACCOUNT_TWEET_FILE = ['Apple', 'AmazonNewsItaly', 'Facebook', 'NetflixIT']


def companies_info():
    h = {}
    with open(settings.COMPANIES_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip header row
        for row in csv_reader:
            if 'ftse' not in row[6] and 'aim' not in row[6]:
                continue
            if row[7] and row[7].lower() not in h.keys():
                h[row[7].lower()] = {'name': row[0], 'isin': row[1]}
    return h


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


def parse_tweet_type(tweet_type):
    return 'official_account' if tweet_type == 'account' else 'hashtag'


def is_mib_company(companies_dict, name):
    return companies_dict.get(name)


def nodes_file():
    companies_dict = companies_info()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    c = 0
    create_directory(today)
    with open(f"/home/marco/Scrivania/tirocinio-unicredit/graphdb/nodes/{today}/tweet_nodes.csv", mode='w') as nodes_file:
        timestamp = oldest_timestamp()
        fieldnames = ['id', 'text', 'sentiment_score', 'date', 'published_by', 'isin', 'organization']
        writer = csv.DictWriter(nodes_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for tweet_type in TWEET_TYPES:
            for dir in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{tweet_type}/"):
                if dir <= timestamp:
                    continue

                for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{tweet_type}/{dir}/"):
                    if is_skipped_tweet_file(filename):
                        continue

                    file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{tweet_type}/{dir}/" + filename)
                    parsed_file = json.load(file)
                    for tweet in parsed_file['data']:
                        print(c)
                        c += 1
                        published_by = parse_tweet_type(tweet_type)
                        node = {
                            'id': tweet['id'],
                            'text': tweet['text'].replace('|', ' '),
                            'sentiment_score': analyze(tweet['text']),
                            'date': parse_date(tweet['created_at']),
                            'published_by': published_by
                        }
                        parsed_file_name = filename.split('.')[0].lower()
                        if published_by == 'official_account' and is_mib_company(companies_dict, parsed_file_name):
                            node['isin'] = companies_dict[parsed_file_name]['isin']
                            node['organization'] = name_parser(companies_dict[parsed_file_name]['name'])
                        else:
                            node['isin'] = None
                            node['organization'] = None
                        writer.writerow(node)
