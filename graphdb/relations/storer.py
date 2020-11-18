import pandas as pd
import csv
import datetime


def typed_rows(df, label_type):
    return df.loc[df['label_type'] == label_type]


def file_path(file_type, label_type):
    base_path = '/home/marco/Scrivania/tirocinio-unicredit/graphdb/relations/'
    if file_type == 'tweet':
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        relation_file_path = f"{base_path}{today}/{file_type}_{label_type}_relations.csv"
    else:
        relation_file_path = f"{base_path}{file_type}_{label_type}_relations.csv"
    return relation_file_path


def store(file_type, file):
    df = pd.read_csv(file, sep='\t')
    for label_type in ['PERSON', 'ORG', 'GPE']:
        with open(file_path(file_type, label_type), mode='w') as relations:
            fieldnames = ['node_id', 'timestamp', 'label_value']
            writer = csv.DictWriter(relations, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            for index, row in typed_rows(df, label_type).iterrows():
                for occurrence in row['occurrences'].split(';'):
                    node_id, timestamp = occurrence.split('|')
                    writer.writerow(
                        {
                            'node_id': node_id,
                            'timestamp': timestamp,
                            'label_value': row['label_value']
                        }
                    )

