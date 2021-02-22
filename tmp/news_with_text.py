import os
import settings
import pandas as pd
import csv
import sys

csv.field_size_limit(sys.maxsize)


def get_text(kgid):
    with open('/home/marco/Scrivania/tirocinio-unicredit/news/kgid_text.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        next(csv_reader)  # skip header row
        for row in csv_reader:
            if row[0] == kgid:
                return row[1]

if __name__ == '__main__':
    c = 0
    directory = '/home/marco/Scrivania/tirocinio-unicredit/news/news_by_isin_to_label'
    for filename in os.listdir(directory):
        c += 1
        df = pd.read_csv(directory + '/' + filename)
        df_len = len(df.index)
        for index, row in df.iterrows():
            print(f"{index}/{df_len} - {c}")
            text = get_text(row['kgid'])
            if not(text):
                continue

            print()
