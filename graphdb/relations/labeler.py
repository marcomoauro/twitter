import pandas as pd
import graphdb.relations.detector as detector
from ner.computer import entities
from stopwords.stopwords import STOPWORDS
from names_dataset import NameDataset
import re
LABELS = ['PERSON', 'ORG', 'GPE']
PATTERN_URL = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'

STOPWORD_THRESHOLD = {
    'tweet': {'ORG': 2, 'GPE': 2},
    'com_stampa': {'ORG': 1, 'GPE': 1}
}


def create_label_dict(file, nlp_detect, nlps, file_type):
    label_dict = {
        'PERSON': {},
        'ORG': {},
        'GPE': {}
    }

    df = pd.read_csv(file, sep='\t')
    print('create label dict')
    name_dataset = NameDataset()
    for index, row in df.iterrows():
        print(index)
        lang = detector.language(row, nlp_detect)
        if not lang or lang not in nlps.keys():
            continue

        doc = nlps[lang](row['text'])
        for ent in doc.ents:#entities(nlps[lang], row['text'], LABELS):
            ent_text = ' '.join(list(filter(None, ent.text.split(' '))))

            if ent.label_ not in LABELS:
                continue

            stopword_count = count_stopwords(ent_text)
            if not contain_at_least_one_alphabet_character(ent_text):
                continue

            if is_bad_text(ent_text):
                continue

            # check for each label type
            if ent.label_ == 'PERSON':
                if not(common_name_or_surname(name_dataset, ent_text)) or stopword_count >= 1:
                    continue

            if ent.label_ == 'ORG':
                if stopword_count >= STOPWORD_THRESHOLD[file_type]['ORG']:
                    continue

            if ent.label_ == 'GPE':
                if stopword_count >= STOPWORD_THRESHOLD[file_type]['GPE']:
                    continue

            label_dict[ent.label_].setdefault(ent_text, []).append((row['id'], row['date']))
    return label_dict


def count_stopwords(text):
    stopword_count = 0
    for word in text.split(' '):
        if word.lower() in STOPWORDS:
            stopword_count += 1

    return stopword_count


def common_name_or_surname(name_dataset, text):
    words = text.split(' ')
    if len(words) <= 1:
        return False

    for word in words:
        if not(name_dataset.search_first_name(word)) and not(name_dataset.search_last_name(word)):
            return False

    return True


def is_bad_text(text):
    if re.search(PATTERN_URL, text):
        return True

    for word in text.split(' '):
        if word[0] in ['#', '&', '@']:
            return True

    return False


def contain_at_least_one_alphabet_character(text):
    return re.search('[a-zA-Z]', text)
