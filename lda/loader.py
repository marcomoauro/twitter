import os
import json
import settings
import csv

TWEET_TYPES = ['hashtag_company', 'account']
COMPANIES_TWEET_FILE = ['apple', 'amazon', 'facebook', 'netflix']
ACCOUNT_TWEET_FILE = ['Apple', 'AmazonNewsItaly', 'Facebook', 'NetflixIT']
AUTHORITATIVE_TWEET_FILE = ['bancacentraleeuropea', 'bancad’inghilterra', 'eurostat', 'georgeosborne','yanisvaroufakis',
                            'stephanieflanders','andrewsentance', 'francescoppola','lionelbarber', 'georgemagnus',
                            'milanofinanza', 'borsaitaliana', 'reuters', 'bloomberg', 'financialtimes', 'kamalahmed',
                            'katiemartin', 'josephfahmy', 'jessefelder', 'albertogallo', 'finanzacom', 'bancad’italia',
                            'blackrock', 'federalreserve', 'exportimportbank', 'wallstreetjournal', 'forbes',
                            'newyorktimes', "ecb", "bankofengland", "EU_eurostat", "George_Osborne", "yanisvaroufakis",
                            "MyStephanomics", "asentance", "frances_coppola", "lionelbarber", "georgemagnus1",
                            "MilanoFinanza", "BorsaItalianaIT", "Reuters", "business", "FT", "bbckamal",
                            "katie_martin_fx", "jfahmy", "jessefelder", "macrocredit", "finanza_com", "bancaditalia",
                            "blackrock", "federalreserve", "EximBankUS", "WSJ", "Forbes", "nytimes"]
PUNCTUATION = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''


def is_skipped_tweet_file(filename):
    name = filename.split('.')[0]
    return name in COMPANIES_TWEET_FILE or name in ACCOUNT_TWEET_FILE


def is_italian_isin(filename, source_dict):
    return source_dict[filename.split('.')[0]][0:2] == 'IT'


def is_authoritative(filename):
    return filename.split('.')[0] in AUTHORITATIVE_TWEET_FILE


def source_file_as_dict():
    csv_file = open(settings.COMPANIES_FILE_PATH)
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    mydict = {rows[7]: rows[1] for rows in csv_reader}
    csv_file = open(settings.COMPANIES_FILE_PATH)
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for rows in csv_reader:
        name = rows[0]
        for c in name:
            if c in PUNCTUATION:
                name = name.replace(c, '')
        name = name.lower()
        mydict.update({name: rows[1]})
    return mydict


def load_data(kind, sources=None):
    data = []
    source_dict = source_file_as_dict()
    for type in TWEET_TYPES:
        for dir in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/"):
            for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/{dir}/"):
                if sources and filename.split('.')[0] not in sources:
                    continue
                if is_skipped_tweet_file(filename):
                    continue
                if kind == 'it' and not is_italian_isin(filename, source_dict):
                    continue
                if kind == 'authoritative' and not is_authoritative(filename):
                    continue
                if kind == 'not_authoritative' and is_authoritative(filename):
                    continue

                file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/{type}/{dir}/" + filename)
                parsed_file = json.load(file)
                data += parsed_file['data']
    return data
