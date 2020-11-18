import spacy
from spacy import displacy
from collections import Counter
from spacy_cld import LanguageDetector
from ner.loader_csv import load_csv
from pprint import pprint
import lda.loader as loader
import en_core_web_sm
import pandas as pd
import lda.cleaner as cleaner
import ner.plotter as plotter
import settings
import csv
import os

PUNCTUATION = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''


def language(tweet, nlp_detect):
    lang = tweet.get('lang')
    if lang:
        return lang
    return detect_language(tweet, nlp_detect)


def detect_language(tweet, nlp_detect):
    try:
        doc = nlp_detect(tweet['url_free_tweets'])
        return doc._.languages[0]
    except Exception as e:
        print(e)
        return None


def start(df, date, name, nlp_detect, nlps, info_type):
    cleaner.clean(df)

    ents = {}
    for index, row in df.iterrows():
        lang = language(row, nlp_detect)
        if not lang or lang not in nlps.keys():
            continue
        doc = nlps[lang](row['url_free_tweets'])
        for ent in doc.ents:
            ents.setdefault(ent.label_, []).append(ent.text)

    plotter.plot(ents, 'summary', date, name, info_type)
    plotter.plot(ents, 'detailed', date, name, info_type)


def normalize_name(row):
    name = row[0]
    for c in name:
        if c in PUNCTUATION:
            name = name.replace(c, '')
    return name.lower()


def ner_tweets(nlp_detect, nlps, date):
    csv_file = open(settings.COMPANIES_FILE_PATH)
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    already_plotted = []
    for row in csv_reader:
        if not (row[7]):
            continue

        name = normalize_name(row)
        if name in already_plotted:
            continue

        already_plotted.append(name)
        data = loader.load_data('all', [name, row[7]])
        if len(data) == 0:
            continue

        print(f"print plot for {name}")
        df = pd.DataFrame(data)
        start(df, date, name, nlp_detect, nlps, 'tweets')

    data = loader.load_data('not_authoritative')
    df = pd.DataFrame(data)
    print('print for all tweets minus that not authoritative')
    start(df, date, 'NOT-AUTHORITATIVE', nlp_detect, nlps, 'tweets')

    data = loader.load_data('all')
    df = pd.DataFrame(data)
    print('final print for all tweets')
    start(df, date, 'ALL', nlp_detect, nlps, 'tweets')


def ner_comunicati_stampa(nlp_detect, nlps, date):
    for filename in os.listdir('/home/marco/Scrivania/tirocinio-unicredit/comunicati/aggregati'):
        df = load_csv(filename)
        try:
            cleaner.clean(df)
            author = df.iloc[0]['author']
            print(f"plot for {author}")
            start(df, date, author, nlp_detect, nlps, 'com_stampa')
        except Exception as e:
            print(e)
            print(f"error for {filename}")


if __name__ == '__main__':
    nlp_detect = spacy.load('en_core_web_lg')
    nlp_detect.add_pipe(LanguageDetector())

    nlps = {
        'it': spacy.load('it_core_news_lg'),
        'en': spacy.load('en_core_web_lg'),
        'fr': spacy.load('fr'),
        'de': spacy.load('de')
    }

    date = '2020-11-10'

    ner_tweets(nlp_detect, nlps, date)
    ner_comunicati_stampa(nlp_detect, nlps, date)
