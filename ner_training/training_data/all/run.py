import pandas as pd
import persone_chiave
import settore
import prodotti
import filiali
import json
from itertools import permutations
import os
from spacy_format.emerging_to_spacy_format import remove_overlapped
from spacy_format.emerging_to_spacy_format import remove_duplicates

LANGUAGE = 'en'  # it, en
KEY_VALUE = 'industry'
ENTITY_LABEL = 'SECTOR'


def fill_labels(language, key_value):
    it_infobox_df = pd.read_csv('/home/marco/Scaricati/it-companies-infobox-properties-final.tsv', sep='\t')
    en_infobox_df = pd.read_csv('/home/marco/Scaricati/en-companies-infobox-properties-final.tsv', sep='\t')
    if language == 'it' and key_value == 'personeChiave':
        return persone_chiave.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'keyPeople':
        return persone_chiave.filler_en(en_infobox_df, key_value)
    if language == 'it' and key_value == 'settore':
        return settore.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'industry':
        return settore.filler_en(en_infobox_df, key_value)
    if language == 'it' and key_value == 'prodotti':
        return prodotti.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'products':
        return prodotti.filler_en(en_infobox_df, key_value)
    if language == 'it' and key_value == 'filiali':
        return filiali.filler_it(it_infobox_df, key_value)
    if language == 'en' and key_value == 'subsid':
        return filiali.filler_en(en_infobox_df, key_value)


def format_company_name(name):
    return name.replace('_', ' ').lower()


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


def get_positions(labels, text_parsed, entity_value):
    positions = []
    label_length = len(labels[0])
    for label in labels:
        index = 0
        while index < len(text_parsed):
            index = text_parsed.find(label, index)
            if index == -1:
                break
            if text_parsed[index - 1] == ' ' and text_parsed[index + label_length] == ' ':
                positions.append((index, index + label_length, entity_value))
            index += label_length
    return positions


def get_labels_perms(label_parsed, entity_value):
    if entity_value != 'KEY_PEOPLE':
        return [label_parsed]
    else:
       return permutation_labels(label_parsed)


def get_text(row, kgids_corrects):
    return row['text']

    corrected_text = kgids_corrects.get(row['kgid'], '')
    if corrected_text != '':
        text = corrected_text
    else:
        text = row['text']
    return text


def get_kgids_corrects():
    kgids = {}
    for news in json.load(open('/home/marco/Scaricati/train.json')):
        kgids[news['kgid']] = news['text'].replace('|', '') + ' '
    for news in json.load(open('/home/marco/Scaricati/test.json')):
        kgids[news['kgid']] = news['text'].replace('|', '') + ' '
    return kgids


def group_same_news_by_kgid(training_data):
    data = []
    train_dict = {}
    for kgid, text, ent_dict in training_data:
        news_dict = train_dict.get(kgid)
        if news_dict:
            news_dict['entities'] += ent_dict['entities']
        else:
            train_dict[kgid] = {
                'entities': ent_dict['entities'],
                'text': text
            }
    for kgid in train_dict.keys():
        all_positions = train_dict[kgid]['entities']
        all_positions = remove_duplicates(all_positions)
        all_positions = remove_overlapped(all_positions)
        data.append((kgid, train_dict[kgid]['text'], {'entities': all_positions}))
    return data


def remove_same_news_by_text(training_data):
    data = []
    train_dict = {}
    for kgid, text, ent_dict in training_data:
        news_dict = train_dict.get(kgid)
        if not news_dict:
            train_dict[text] = {
                'entities': ent_dict['entities'],
                'kgid': kgid
            }
    for text in train_dict.keys():
        data.append((train_dict[text]['kgid'], text, {'entities': train_dict[text]['entities']}))
    return data


if __name__ == '__main__':
    kgids_corrects = get_kgids_corrects()
    labels_by_company = fill_labels(LANGUAGE, KEY_VALUE)
    companies_infobox = labels_by_company.keys()
    training_data = []
    f = 0
    c = 0
    directory = '/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/kgid-title-text-url-langfull'
    for filename in os.listdir(directory):
        f += 1
        company = format_company_name(filename.split('.')[0])
        df = pd.read_csv(f"{directory}/{filename}", sep='|')
        len_df = len(df.index)
        for index, row in df.iterrows():
            c += 1
            print(f"{index}/{len_df} - {f} - {c}")
            language = row.get('language') or row.get('lang')
            if language != LANGUAGE:
                continue

            if company not in companies_infobox:
                continue

            if len(row['text']) > 50000:
                continue

            raw_text = get_text(row, kgids_corrects)
            text_parsed = format_text(raw_text)
            dict_company = labels_by_company[company]
            all_positions = []
            for entity_value in dict_company.keys():
                labels = list(filter(None, dict_company[entity_value]))
                if labels == []:
                    continue

                for label in labels:
                    label_parsed = format_text(label)
                    labels_perms = get_labels_perms(label_parsed, entity_value)

                    positions = get_positions(labels_perms, text_parsed, entity_value)
                    if len(positions) > 0:
                        all_positions += positions
            if len(all_positions) > 0:
                all_positions = remove_duplicates(all_positions)
                all_positions = remove_overlapped(all_positions)
                training_data.append((row['kgid'], raw_text + '.', {'entities': all_positions}))
    training_data = group_same_news_by_kgid(training_data)
    training_data = remove_same_news_by_text(training_data)
    with open(f"/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/{LANGUAGE.lower()}_{KEY_VALUE.lower()}_data.json", 'w') as outfile:
        json.dump(training_data, outfile)
