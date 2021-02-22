import os
import spacy
from spacy_cld import LanguageDetector
import pandas as pd
import csv


def detect_language(text, nlp_detect):
    try:
        doc = nlp_detect(text)
        return doc._.languages[0]
    except Exception as e:
        return None


if __name__ == '__main__':
    nlp_detect = spacy.load('en_core_web_lg')
    nlp_detect.add_pipe(LanguageDetector())
    directory = '/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/kgid-title-text-url-lang'
    c = 0
    for filename in os.listdir(directory):
        if filename in os.listdir('/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/kgid-title-text-url-langfull'):
            continue

        df = pd.read_csv(directory+'/'+filename, sep='|')
        with open(f"/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/kgid-title-text-url-langfull/{filename}", mode='w') as lang_file:
            fieldnames = ['kgid', 'text', 'language', 'title', 'url']
            writer = csv.DictWriter(lang_file, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            for index, row in df.iterrows():
                c += 1
                if c % 1000 == 0:
                    print(c)
                title = row['title']
                language = detect_language(title, nlp_detect) if str(row['lang']) == 'nan' else row['lang']
                if not language:
                    continue

                if language != 'it' and language != 'en':
                    continue

                writer.writerow(
                    {
                        'kgid': row['kgid'],
                        'language': language,
                        'text': row['text'],
                        'title': title,
                        'url': row['url']
                    }
                )
