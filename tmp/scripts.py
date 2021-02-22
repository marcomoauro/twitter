import os
import spacy
from spacy_cld import LanguageDetector
import pandas as pd


def parse_doc(nlp_detect, text):
    try:
        return nlp_detect(text)
    except Exception as e:
        print(e)
        return None


def has_more_languages(doc):
    try:
        return len(doc._.languages) == 2 and doc._.language_scores[doc._.languages[0]] < 0.8
    except Exception as e:
        print(e)
        return None


nlp_detect = spacy.load('en_core_web_lg')
nlp_detect.add_pipe(LanguageDetector())
aggregati_path = '/home/marco/Scrivania/tirocinio-unicredit/comunicati/aggregati'
tot = 0
double_langs = 0
double_langs_files = []
for filename in os.listdir(aggregati_path):
    df = pd.read_csv(aggregati_path + '/' + filename, sep='|')
    for index, row in df.iterrows():
        tot += 1
        print(tot)
        doc = parse_doc(nlp_detect, row['text'])
        if has_more_languages(doc):
            double_langs += 1
            double_langs_files.append(filename)
miao = 0


t1=t[0:int(len(t)/2)]
t2=t[int(len(t)/2):]
doc1 = nlp_detect(t1)
doc2 = nlp_detect(t2)
print(doc1._.language_scores)
print(doc2._.language_scores)