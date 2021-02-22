import os
import spacy
from spacy_cld import LanguageDetector
import pandas as pd
import csv


def get_fields(row, isin):
    return {
        'title':      row['title'],
        'href':       row['href'],
        'date':       row['date'],
        'author':     row['author'],
        'crawl_date': row['crawl_date'],
        'pdfID':      row['pdfID'],
        'pdfURL':     row['pdfURL'],
        'isin':       isin
    }


def get_lang(doc):
    return doc._.languages[0]


def has_bilang(doc, doc1, doc2):
    if len(doc._.languages) == 1:
        return False

    lang1 = get_lang(doc1)
    lang2 = get_lang(doc2)
    return lang1 != lang2 and doc1._.language_scores[lang1] > 0.7 and doc2._.language_scores[lang2] > 0.7


c = 0
nlp_detect = spacy.load('en_core_web_lg')
nlp_detect.add_pipe(LanguageDetector())
aggregati_path = '/home/marco/Scrivania/tirocinio-unicredit/comunicati/aggregati'
with open('/home/marco/Scrivania/tirocinio-unicredit/ner-trained/com_stampa_with_lang.csv', mode='w') as com_stampa_file:
    fieldnames = ['isin', 'language', 'author', 'title', 'href', 'date', 'crawl_date', 'pdfID', 'pdfURL', 'text']
    writer = csv.DictWriter(com_stampa_file, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()
    for filename in os.listdir(aggregati_path):
        df = pd.read_csv(aggregati_path + '/' + filename, sep='|')
        try:
            for index, row in df.iterrows():
                c += 1
                print(c)
                text = row['text'].replace('|', ' ')
                fields = get_fields(row, filename.split('_')[0])
                doc = nlp_detect(text)
                text1 = text[0:int(len(text)/2)]
                text2 = text[int(len(text)/2):]
                doc1 = nlp_detect(text1)
                doc2 = nlp_detect(text2)
                lang = get_lang(doc)
                lang1 = get_lang(doc1)
                lang2 = get_lang(doc2)
                if has_bilang(doc, doc1, doc2):
                    fields.update({'text': text1, 'language': lang1})
                    writer.writerow(fields)
                    fields.update({'text': text2, 'language': lang2})
                    writer.writerow(fields)
                else:
                    fields.update({'text': text, 'language': lang})
                    writer.writerow(fields)
        except Exception as e:
            print(e)
            continue
