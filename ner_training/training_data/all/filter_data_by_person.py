import json


if __name__ == '__main__':
    file = open('/home/marco/Scrivania/tirocinio-unicredit/news/all/training_data/en-sector/train_sector.txt', 'r')
    lines = file.readlines()
    spacy_docs = []
    train_c = 0
    train_persons = []
    for line in lines:
        line = line.strip()
        splitted_line = list(filter(None, line.split(' ')))
        train_c += int(splitted_line[0])
        train_persons.append(' '.join(splitted_line[2:]))

    file = open('/home/marco/Scrivania/tirocinio-unicredit/news/all/training_data/en-sector/test_sector.txt', 'r')
    lines = file.readlines()
    spacy_docs = []
    test_c = 0
    test_persons = []
    for line in lines:
        line = line.strip()
        splitted_line = list(filter(None, line.split(' ')))
        test_c += int(splitted_line[0])
        test_persons.append(' '.join(splitted_line[2:]))

    train = []
    test = []
    data = json.load(open('/home/marco/Scrivania/tirocinio-unicredit/news/all/training_data/en-sector/data.json'))
    for record in data:
        text = record[1]
        ents = record[2]['entities']
        values = []
        for start, end, _ in ents:
            values.append(text[start:end].lower())
        for value in values:
            if value in train_persons:
                train.append(record)
                break
            if value in test_persons:
                test.append(record)
                break
    with open(f"/home/marco/Scrivania/tirocinio-unicredit/news/all/training_data/en-sector/subset/train.json", 'w') as outfile:
        json.dump(train, outfile)
    with open(f"/home/marco/Scrivania/tirocinio-unicredit/news/all/training_data/en-sector/subset/test.json", 'w') as outfile:
        json.dump(test, outfile)
