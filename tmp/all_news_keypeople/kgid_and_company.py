import pandas as pd
import os
import csv


def format_name(name):
    return name.replace('_', ' ').lower()


def companies(infobox_path):
    df = pd.read_csv(infobox_path, sep='\t')
    ns = []
    for name_raw in list(set(df['Resource'])):
        name = format_name(name_raw)
        ns.append(name)
    return ns


if __name__ == '__main__':
    cs_en = companies('/home/marco/Scaricati/en-companies-infobox-properties-final.tsv')
    cs_it = companies('/home/marco/Scaricati/it-companies-infobox-properties-final.tsv')
    cs = list(set(cs_it + cs_en))
    file_data = '/home/marco/Scaricati/expanded-companies-gdelt/expanded-gdelt-2020-0102-news2organization-relations.csv'
    c = 0
    with open('/home/marco/Scrivania/tirocinio-unicredit/news/all-keypeople/kgid_company.csv', mode='w') as news_file:
        fieldnames = ['kgid', 'company']
        writer = csv.DictWriter(news_file, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        df = pd.read_csv(file_data, sep='\t')
        for index, row in df.iterrows():
            company_raw = row.get('organization')
            company = format_name(company_raw)
            if company in cs:
                c += 1
                if c % 1000 == 0:
                    print(c)
                writer.writerow(
                    {
                        'kgid': row['news'],
                        'company': company_raw
                    }
                )
