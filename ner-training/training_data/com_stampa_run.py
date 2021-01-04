import pandas as pd
import persone_chiave
import filiali
import settore
import prodotti
import sede
import settings
import json
from itertools import permutations

LANGUAGE = 'it'
KEY_VALUE = 'personeChiave'
ENTITY_LABEL = 'KEY_PEOPLE'


def fill_labels(language, key_value):
    it_infobox_df = pd.read_csv('/home/marco/Scrivania/tirocinio-unicredit/ner-trained/itwiki-infobox-properties-final.tsv', sep='\t')
    en_infobox_df = pd.read_csv('/home/marco/Scrivania/tirocinio-unicredit/ner-trained/enwiki-infobox-properties-final.tsv', sep='\t')
    if language == 'it' and key_value == 'personeChiave':
        return persone_chiave.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'keyPeople':
        return persone_chiave.filler_en(en_infobox_df, key_value)
    if language == 'it' and key_value == 'filiali':
        return filiali.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'subsid':
        return filiali.filler_en(en_infobox_df, key_value)
    if language == 'it' and key_value == 'settore':
        return settore.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'industry':
        return settore.filler_en(en_infobox_df, key_value)
    if language == 'it' and key_value == 'prodotti':
        return prodotti.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'products':
        return prodotti.filler_en(en_infobox_df, key_value)
    if language == 'it' and key_value == 'sede':
        return sede.filler_it(it_infobox_df, key_value)
    if language == 'en' and ENTITY_LABEL == 'HEADQUARTER':
        return sede.filler_en(en_infobox_df)


def get_isin_to_company():
    d = {}
    df = pd.read_csv(settings.COMPANIES_FILE_PATH)
    for index, row in df.iterrows():
        d[row['ISIN']] = row['Nome'].lower()
    return d


def format_text(text):
    return text.lower()


def permutation_labels(label):
    perms_labels = []
    array_label = label.split(' ')
    perms = list(permutations(range(0, len(array_label))))
    for perm in perms:
        l = []
        for i in perm:
            l.append(array_label[i])
        perms_labels.append(' '.join(l))
    return perms_labels


def get_positions(labels, text_parsed):
    positions = []
    label_length = len(labels[0])
    for label in labels:
        index = 0
        while index < len(text_parsed):
            index = text_parsed.find(label, index)
            if index == -1:
                break
            if text_parsed[index - 1] == ' ' and text_parsed[index + label_length] == ' ':
                positions.append((index, index + label_length, ENTITY_LABEL))
            index += label_length
    return positions


def get_labels_perms(label_parsed):
    if ENTITY_LABEL != 'KEY_PEOPLE':
        return [label_parsed]
    else:
       return permutation_labels(label_parsed)


if __name__ == '__main__':
    labels_by_company = fill_labels(LANGUAGE, KEY_VALUE)
    companies_infobox = labels_by_company.keys()
    isin_to_company = get_isin_to_company()
    df = pd.read_csv('/home/marco/Scrivania/tirocinio-unicredit/ner-trained/com_stampa_with_lang.csv', sep='|')
    training_data = []
    for index, row in df.iterrows():
        print(index)
        if row['language'] != LANGUAGE:
            continue

        company = isin_to_company.get(row['isin'])
        if not company:
            continue

        if company not in companies_infobox:
            continue

        labels = list(set(labels_by_company[company]))
        for label in labels:
            label_parsed = format_text(label)
            text_parsed = format_text(row['text'])
            labels_perms = get_labels_perms(label_parsed)

            positions = get_positions(labels_perms, text_parsed)
            if len(positions) > 0:
                training_data.append((row['text'] + '.', {'entities': positions}))
    with open(f"/home/marco/Scrivania/tirocinio-unicredit/ner-trained/training-data/{LANGUAGE.lower()}_{KEY_VALUE.lower()}_training_data.json", 'w') as outfile:
        json.dump(training_data, outfile)
