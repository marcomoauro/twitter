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
    directory = '/home/marco/Scrivania/tirocinio-unicredit/news/news_by_isin_to_label_with_text'
    f = 0
    c = 0
    for filename in os.listdir(directory):
        if filename in os.listdir('/home/marco/Scrivania/tirocinio-unicredit/news/news_with_lang'):
            continue

        f += 1
        df = pd.read_csv(directory+'/'+filename, sep='|')
        len_df = len(df.index)
        with open(f"/home/marco/Scrivania/tirocinio-unicredit/news/news_with_lang/{filename}", mode='w') as lang_file:
            fieldnames = ['kgid', 'text', 'language', 'title']
            writer = csv.DictWriter(lang_file, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            for index, row in df.iterrows():
                c += 1
                print(f"{index}/{len_df} - {f} -- {c}")
                title = row['title']
                language = detect_language(title, nlp_detect)
                if not language:
                    continue

                if language != 'it' and language != 'en':
                    continue

                writer.writerow(
                    {
                        'kgid': row['kgid'],
                        'language': language,
                        'text': row['text'],
                        'title': title
                    }
                )
