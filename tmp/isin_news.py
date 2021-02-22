import os
import pandas as pd
import csv


with open('/home/marco/Scrivania/tirocinio-unicredit/news/news_isin.csv', mode='w') as news_file:
    fieldnames = ['kgid', 'isin']
    writer = csv.DictWriter(news_file, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()
    directory = '/home/marco/Scrivania/tirocinio-unicredit/news/gdelt-neo4j'
    f = 0
    for filename in os.listdir(directory):
        c = 0
        if 'news2mib-relations' not in filename:
            continue

        df = pd.read_csv(directory + '/' + filename, sep='\t')
        f += 1
        for index, row in df.iterrows():
            c += 1
            print(f"{c}/{len(df.index)} - {f}")
            kgid = row['news']
            isin = row['isin']
            if not kgid or not isin:
                continue

            writer.writerow(
                {
                    'kgid': kgid,
                    'isin': isin
                }
            )
