import csv
import datetime
import os


def parse_occurrences(occ):
    s = f"{occ[0][0]}|{occ[0][1]}"
    for o in occ[1:]:
        s += f";{o[0]}|{o[1]}"
    return s


def create_directory(date):
    directory_path = f"/home/marco/Scrivania/tirocinio-unicredit/graphdb/relations/{date}/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def store(file_type, label_dict):
    base_path = '/home/marco/Scrivania/tirocinio-unicredit/graphdb/relations/'
    if file_type == 'tweet':
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        create_directory(today)
        temp_relation_file_path = base_path + today + '/temp_tweet_relations.csv'
    else:
        temp_relation_file_path = base_path + '/temp_com_stampa_relations.csv'

    print(f"create {file_type} temp relations file")
    with open(temp_relation_file_path, mode='w') as temp_relations:
        fieldnames = ['label_type', 'label_value', 'occurrences']
        writer = csv.DictWriter(temp_relations, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for label_type in label_dict.keys():
            for label_value in label_dict[label_type].keys():
                occ = label_dict[label_type][label_value]
                writer.writerow(
                    {
                        'label_type': label_type,
                        'label_value': label_value,
                        'occurrences': parse_occurrences(occ)
                    }
                )


def store_discarded_labels(file_type, discarded_labels):
    base_path = '/home/marco/Scrivania/tirocinio-unicredit/graphdb/relations/'
    if file_type == 'tweet':
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        create_directory(today)
        temp_relation_discarded_file_path = base_path + today + '/temp_tweet_relations_discarded.csv'
    else:
        temp_relation_discarded_file_path = base_path + '/temp_com_stampa_relations_discarded.csv'

    print(f"create {file_type} temp relations discarded file")
    with open(temp_relation_discarded_file_path, mode='w') as temp_relations_discarded:
        fieldnames = ['label_type', 'label_value', 'reason']
        writer = csv.DictWriter(temp_relations_discarded, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for dl in discarded_labels:
            writer.writerow(
                {
                    'label_type': dl[0],
                    'label_value': dl[1],
                    'reason': dl[2]
                }
            )
