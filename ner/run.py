import spacy
from spacy import displacy
from collections import Counter
from spacy_cld import LanguageDetector
from pprint import pprint
import lda.loader as loader
import en_core_web_sm
import pandas as pd
import lda.cleaner as cleaner
import ner.plotter as plotter
import settings
import csv

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


def start(data, date, name, nlp_detect, nlps):
    df = pd.DataFrame(data)
    cleaner.clean(df)

    ents = {}
    for index, row in df.iterrows():
        lang = language(row, nlp_detect)
        if not lang or lang not in nlps.keys():
            continue
        doc = nlps[lang](row['url_free_tweets'])
        for ent in doc.ents:
            ents.setdefault(ent.label_, []).append(ent.text)

    plotter.plot(ents, 'summary', date, name)
    plotter.plot(ents, 'detailed', date, name)


def normalize_name(row):
    name = row[0]
    for c in name:
        if c in PUNCTUATION:
            name = name.replace(c, '')
    return name.lower()


if __name__ == '__main__':
    nlp_detect = spacy.load('en')
    nlp_detect.add_pipe(LanguageDetector())

    nlps = {
        'it': spacy.load('it'),
        'en': spacy.load('en'),
        'fr': spacy.load('fr'),
        'de': spacy.load('de')
    }

    date = '2020-11-09'

    csv_file = open(settings.COMPANIES_FILE_PATH)
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    already_plotted = []
    for row in csv_reader:
        if not(row[7]):
            continue

        name = normalize_name(row)
        if name in already_plotted:
            continue

        already_plotted.append(name)
        data = loader.load_data('all', [name, row[7]])
        if len(data) == 0:
            continue

        print(f"print plot for {name}")
        start(data, date, name, nlp_detect, nlps)

    data = loader.load_data('not_authoritative')
    print('print for all tweets minus that not authoritative')
    start(data, date, 'NOT-AUTHORITATIVE', nlp_detect, nlps)

    data = loader.load_data('all')
    print('final print for all tweets')
    start(data, date, 'ALL', nlp_detect, nlps)
