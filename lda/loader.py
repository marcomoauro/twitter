import os
import json

TWEET_KINDS = ['hashtag_company', 'account']


def load_data():
    data = []
    for kind in TWEET_KINDS:
        for dir in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{kind}/"):
            for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{kind}/{dir}/"):
                file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{kind}/{dir}/" + filename)
                parsed_file = json.load(file)
                data += parsed_file['data']
    return data
