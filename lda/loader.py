import os
import json


def load_data():
    data = []
    for dir in os.listdir('/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag_company/'):
        for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag_company/{dir}/"):
            file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag_company/{dir}/" + filename)
            parsed_file = json.load(file)
            data += parsed_file['data']
    return data
