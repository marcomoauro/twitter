import os
import spacy
from spacy_cld import LanguageDetector
import pandas as pd
import csv
import json


def detect_language(text, nlp_detect):
    try:
        doc = nlp_detect(text)
        return doc._.languages[0]
    except Exception as e:
        return None


if __name__ == '__main__':
    nlp_detect = spacy.load('en_core_web_lg')
    nlp_detect.add_pipe(LanguageDetector())
    with open('/home/marco/Scrivania/tirocinio-unicredit/news/news_with_lang.csv', mode='w') as news_file:
        fieldnames = ['kgid', 'text']
        writer = csv.DictWriter(news_file, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        directory = '/home/marco/Scrivania/tirocinio-unicredit/news/gdelt-crawled-content'
        f = 0
        for filename in os.listdir(directory):
            c = 0
            if filename.split('.')[-1] != 'json':
                continue

            news_chunk = json.load(open(directory + '/' + filename))
            f += 1
            file_size = len(news_chunk)
            for news in news_chunk:
                c += 1
                print(f"{c}/{file_size} - {f}")
                kgid = news.get('kgid')
                text = news.get('text')
                if not kgid or not text:
                    continue

                #language = detect_language(text, nlp_detect)
                #if not language:
                #    continue

                #if language != 'it' or language != 'en':
                #    continue

                writer.writerow(
                    {
                        'kgid':     kgid,
                        #'language': language,
                        'text':     text.replace('|', ' ')
                    }
                )
