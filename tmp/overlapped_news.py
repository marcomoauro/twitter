import json


if __name__ == '__main__':
    c = 0
    data = json.load(open('/home/marco/Scrivania/tirocinio-unicredit/news/training-data/en/keypeople/data.json'))
    for text, ents in data:
        values = []
        for ent in ents['entities']:
            label = text[ent[0]:ent[1]].lower()
            values.append(label)
        unique_values = list(set(values))
        if len(unique_values) > 1:
            c += 1
    print(f"{c}/{len(data)}")
