import json
import random

def get_new_label(length):
    if length == 8:
        arr = ['Cora Teo', 'Dina Mil', 'Elsa Per', 'Teo Milo']
    if length == 10:
        arr = ['Marco Pera', 'Alida Fert', 'Delia Mili', 'Erika Nulo']
    if length == 12:
        arr = ['Sara Fratter', 'Livio Maitan', 'Jesus Christ', 'John Cenalop']
    if length == 13:
        arr = ['Paola Brander', 'Omero Molpito', 'Manuel Arcuri', 'Paolo Menital']
    if length == 14:
        arr = ['Gianluca Centi', 'Raluca Metrola', 'Martino Primot', 'Francesca Pulo']
    if length == 15:
        arr = ['Lorenzo Melossi', 'Valentina Misto', 'Valerio Rossini', 'Federica Mistro']
    if length == 18:
        arr = ['Damiano Altezzosti', 'Angelo Petagnartri', 'Alessandro Moauron', 'Gabriele Vincenzon']
    return random.choice(arr)


if __name__ == '__main__':
    train_set = json.load(open('/home/marco/Scrivania/tirocinio-unicredit/news/training-data/en/keypeople/train_unique.json'))
    new_train_set = []
    lengths = set()
    for news, ents_dict in train_set:
        ents = ents_dict['entities']
        temp_news = news
        for start, end, named_entity in ents:
            label = temp_news[start:end]
            lengths.add(len(label))
            new_label = get_new_label(len(label))
            news = news.replace(label, new_label)
        new_train_set.append([news, {'entities': ents}])
    with open('/home/marco/Scrivania/tirocinio-unicredit/news/training-data/en/keypeople/train_placeholder.json', 'w') as f:
        json.dump(new_train_set, f)
