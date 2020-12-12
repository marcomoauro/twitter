import pandas as pd
import graphdb.relations.detector as detector
from stopwords.stopwords import STOPWORDS
from names_dataset import NameDataset
import re
from stopwords.it_cw import IT_CW
from stopwords.en_cw import EN_CW
WHITELISTED_WORDS = ['USA', 'US']
LABELS = ['PERSON', 'ORG', 'GPE']
PATTERN_URL = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
COMMON_WORDS_DATASET = EN_CW + IT_CW
from graphdb.relations.common.person import COMMON_NAMES_AND_SURNAMES
from graphdb.relations.common.organization import COMMON_ORGANIZATIONS
from graphdb.relations.common.location import COMMON_LOCATIONS
NAME_DATASET = NameDataset()

def create_label_dict(file, nlp_detect, nlps, file_type):
    label_dict = {
        'PERSON': {},
        'ORG': {},
        'GPE': {}
    }
    discarded_labels = []

    df = pd.read_csv(file, sep='\t')
    print('create label dict')
    for index, row in df.iterrows():
        print(index)
        lang = detector.language(row, nlp_detect)
        if not lang or lang not in nlps.keys():
            continue

        doc = nlps[lang](row['text'])
        for ent in doc.ents:
            ent_text = beautify_text(ent.text)

            if ent.label_ not in LABELS:
                continue

            if not contain_at_least_one_alphabet_character(ent_text):
                discarded_labels.append([ent.label_, ent_text, 'no_alphabet_characters'])
                continue

            if is_bad_text(ent_text):
                discarded_labels.append([ent.label_, ent_text, 'bad_text'])
                continue

            # check for each label type
            if ent.label_ == 'PERSON' and not is_common_person(ent_text):
                if count_stopwords(ent_text) >= 1:
                    discarded_labels.append([ent.label_, ent_text, 'stopword_count >= 1'])
                    continue

            if ent.label_ == 'ORG' and not is_common_organization(ent_text):
                if not is_contain_uncommon_words(ent_text):
                    discarded_labels.append([ent.label_, ent_text, 'not contain uncommon words'])
                    continue

            if ent.label_ == 'GPE' and not is_common_location(ent_text):
                if not is_contain_uncommon_words(ent_text):
                    discarded_labels.append([ent.label_, ent_text, 'not contain uncommon words'])
                    continue

            label_dict[ent.label_].setdefault(ent_text, []).append((row['id'], row['date']))
    return label_dict, discarded_labels


def beautify_text(text):
    new_text = []
    for word in text.split(' '):
        if not word:
            continue
        if len(word) == 1 and word in ['#', '&', '@']:
            continue
        if len(word) > 1 and word[0] in ['#', '&', '@']:
            new_text.append(word[1:])
        else:
            new_text.append(word)

    return ' '.join(new_text)


def count_stopwords(text):
    stopword_count = 0
    for word in text.split(' '):
        if word.lower() in STOPWORDS:
            stopword_count += 1

    return stopword_count


def is_common_person(text):
    for word in text.split(' '):
        if not(NAME_DATASET.search_first_name(word)) and not(NAME_DATASET.search_last_name(word)) and word.lower() not in COMMON_NAMES_AND_SURNAMES:
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


def is_contain_uncommon_words(text):
    words = text.split(' ')
    if len(words) == 1 and words[0] in WHITELISTED_WORDS:
        return True
    if is_capitalized(text):
        return True
    for word in words:
        lower_word = word.lower()
        if lower_word not in COMMON_WORDS_DATASET:
            return True
    return False


def is_capitalized(text):
    count = 0
    words = text.split(' ')
    for word in words:
        if word.istitle():
            count += 1
    return count/len(words) > 0.4


def is_common_organization(text):
    return text.lower() in COMMON_ORGANIZATIONS


def is_common_location(text):
    return text.lower() in COMMON_LOCATIONS
