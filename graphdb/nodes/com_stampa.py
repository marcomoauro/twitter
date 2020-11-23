import os
import pandas as pd
import csv
from sentiment_analysis.run import analyze


def clean_text(text):
    text_without_punct = text.replace("\n", ' ').replace("\t", ' ').replace('/', ' ').replace('\uf0b7', ' ').replace('\xa0', ' ').replace('“', ' ').strip()
    return ' '.join(list(filter(None, text_without_punct.split(' '))))


def clean_date(row_date):
    return row_date.replace("\n", '').replace("\t", '').replace('\r', '').strip()


def nodes_file():
    c = 0
    with open('/home/marco/Scrivania/tirocinio-unicredit/graphdb/nodes/com_stampa_nodes.csv', mode='w') as nodes_file:
        fieldnames = ['id', 'text', 'sentiment_score', 'date']
        writer = csv.DictWriter(nodes_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for filename in os.listdir('/home/marco/Scrivania/tirocinio-unicredit/comunicati/aggregati'):
            if filename[0] == '.':
                continue

            df = pd.read_csv('/home/marco/Scrivania/tirocinio-unicredit/comunicati/aggregati/' + filename, sep='|')
            for index, row in df.iterrows():
                c += 1
                print(c)
                try:
                    writer.writerow(
                        {
                            'id': filename.split('_')[0] + '-' + str(row['pdfID']),
                            'text': clean_text(row['text']),
                            'sentiment_score': analyze(row['text']),
                            'date': clean_date(row['date'])
                        }
                    )
                except Exception as e:
                    print(e)
                    print(filename)
                    print(index)
