import pandas as pd
import persone_chiave
import filiali
import settore
import prodotti
import sede
import settings
import json
from itertools import permutations
import os
from spacy_format.emerging_to_spacy_format import remove_overlapped
from spacy_format.emerging_to_spacy_format import remove_duplicates

LANGUAGE = 'en'  # it, en
KEY_VALUE = 'keyPeople'
ENTITY_LABEL = 'SUBSID'  # KEY_PEOPLE, SUBSID, SECTOR, PRODUCT, HEADQUARTER


def fill_labels(language, key_value):
    it_infobox_df = pd.read_csv('/home/marco/Scrivania/tirocinio-unicredit/ner-trained/itwiki-infobox-properties-final.tsv', sep='\t')
    en_infobox_df = pd.read_csv('/home/marco/Scaricati/en-companies-infobox-properties-final.tsv', sep='\t')
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
    # if language == 'it' and key_value == 'sede':
    #    return sede.filler_it(it_infobox_df, key_value)
    # if language == 'en' and ENTITY_LABEL == 'HEADQUARTER':
    #    return sede.filler_en(en_infobox_df)
    if language == 'en' and key_value == 'all':
        persone_chiave_dict = persone_chiave.filler_en(en_infobox_df, 'keyPeople')
        prodotti_dict = prodotti.filler_en(en_infobox_df, 'products')
        filiali_dict = filiali.filler_en(en_infobox_df, 'subsid')
        settore_dict = settore.filler_en(en_infobox_df, 'industry')
        all_dict = {}
        for agency in sorted(list(set(list(persone_chiave_dict.keys()) + list(prodotti_dict.keys()) + list(filiali_dict.keys()) + list(settore_dict.keys())))):
            agency_dict = {}
            pc = persone_chiave_dict.get(agency)
            if pc:
                agency_dict['KEY_PEOPLE'] = pc
            p = prodotti_dict.get(agency)
            if p:
                agency_dict['PRODUCT'] = p
            f = filiali_dict.get(agency)
            if f:
                agency_dict['SUBSID'] = f
            s = settore_dict.get(agency)
            if s:
                agency_dict['SECTOR'] = s
            if agency_dict != {}:
                all_dict[agency] = agency_dict
        return all_dict

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


if __name__ == '__main__':
    labels_by_company = fill_labels(LANGUAGE, KEY_VALUE)
    companies_infobox = labels_by_company.keys()
    isin_to_company = get_isin_to_company()
    training_data = []
    f = 0
    c = 0
    for filename in os.listdir('/home/marco/Scrivania/tirocinio-unicredit/news/news_with_lang'):
        f += 1
        isin = filename.split('.')[0]
        df = pd.read_csv(f"/home/marco/Scrivania/tirocinio-unicredit/news/news_with_lang/{filename}", sep='|')
        len_df = len(df.index)
        for index, row in df.iterrows():
            c += 1
            print(f"{index}/{len_df} - {f} - {c}")
            if row['language'] != LANGUAGE:
                continue

            company = isin_to_company.get(isin)
            if company not in companies_infobox:
                continue

            text_parsed = format_text(row['text'])
            dict_company = labels_by_company[company]
            all_positions = []
            for entity_value in dict_company.keys():
                labels = dict_company[entity_value]
                for label in labels:
                    label_parsed = format_text(label)
                    labels_perms = get_labels_perms(label_parsed, entity_value)

                    positions = get_positions(labels_perms, text_parsed, entity_value)
                    if len(positions) > 0:
                        all_positions += positions
            if len(all_positions) > 0:
                all_positions = remove_duplicates(all_positions)
                all_positions = remove_overlapped(all_positions)
                training_data.append((row['text'] + '.', {'entities': all_positions}))
    with open(f"/home/marco/Scrivania/tirocinio-unicredit/news/training-data/{LANGUAGE.lower()}_{KEY_VALUE.lower()}_training_data.json", 'w') as outfile:
        json.dump(training_data, outfile)
