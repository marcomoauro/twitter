import json


def get_label_value(text, ents):
    values = []
    for ent in ents['entities']:
        label = text[ent[0]:ent[1]].lower()
        values.append(label)
    unique_values = list(set(values))
    return unique_values[0]


if __name__ == '__main__':
    train = []
    test = []
    train_label = ['reed hastings', 'guillaume faury', 'bob swan', 'michael corbat', 'joe kaeser', 'oliver zipse', 'martin zielke', 'stefan schmittmann']
    data = json.load(open('/home/marco/Scrivania/tirocinio-unicredit/news/training-data/en/keypeople/data.json'))
    for record in data:
        train.append(record) if get_label_value(record[0], record[1]) in train_label else test.append(record)
    with open('/home/marco/Scrivania/tirocinio-unicredit/news/training-data/en/keypeople/train_unique.json', 'w') as f:
        json.dump(train, f)
    with open('/home/marco/Scrivania/tirocinio-unicredit/news/training-data/en/keypeople/test_unique.json', 'w') as f:
        json.dump(test, f)
