import random
from wordfreq import random_words
BAD_COMMON_WORDS = ['entertainment','internet','advertising','retail','insurance','software','clothing','music','film','restaurants','social','industry','security','manufacturing','engineering','transport','construction','mining','defence']
COMMON_WORDS = list(set(random_words(lang='en', wordlist='best', nwords=100000).split(' ')))
for bw in BAD_COMMON_WORDS:
    COMMON_WORDS.remove(bw)
from names_dataset import NameDataset
d = NameDataset()
NAMES = list(d.first_names)
SURNAMES = list(d.last_names)
ALPHABET = ['a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','y','z', ' ', ' ', ' ', ' ']


def get_placeholder(size):
    return ''.join(random.choices(ALPHABET, k=size))


def get_bool_rand():
    return random.choice([True, False])


def get_placeholder_name_and_surname(size):
    try:
        for i in range(100):
            name = random.choice(NAMES)
            surname = random.choice(SURNAMES)
            if get_bool_rand():
                name = name.capitalize()
            if get_bool_rand():
                surname = surname.capitalize()
            arr = [name, surname]
            random.shuffle(arr)
            placeholder = ' '.join(arr)
            if len(placeholder) == size:
                return placeholder
            if get_bool_rand():
                name = random.choice(list(filter(lambda x: len(x) == size, NAMES)))
                if get_bool_rand():
                    name = name.capitalize()
                return name
            else:
                surname = random.choice(list(filter(lambda x: len(x) == size, SURNAMES)))
                if get_bool_rand():
                    surname = surname.capitalize()
                return surname
    except:
        return get_placeholder(size)


def get_two_words(size):
    if (size % 2) == 0:
        size1 = size / 2
        size2 = size1 - 1
    else:
        size1 = int(size/2)
        size2 = size1
    word1 = random.choice(list(filter(lambda x: len(x) == size1, COMMON_WORDS)))
    word2 = random.choice(list(filter(lambda x: len(x) == size2, COMMON_WORDS)))
    if get_bool_rand():
        word1 = word1.capitalize()
    if get_bool_rand():
        word2 = word2.capitalize()
    return word1 + ' ' + word2


def get_placeholder_common_name(size):
    try:
        if size >= 16:
            return get_two_words(size)
        else:
            word = random.choice(list(filter(lambda x: len(x) == size, COMMON_WORDS)))
            if get_bool_rand():
                word = word.capitalize()
            return word
    except:
        return get_placeholder(size)


def test_with_placeholder(data):
    new_data = []
    for kgid, text, ents in data:
        pl_text = text
        for start, end, label in ents['entities']:
            placeholder = get_placeholder(end - start)
            pl_text = pl_text[:start] + placeholder + pl_text[end:]
        new_data.append([kgid, text, ents, pl_text])
    return new_data


def test_with_placeholder_name_and_surname(data):
    new_data = []
    c = 0
    len_data = len(data)
    for kgid, text, ents in data:
        c += 1
        print(f"create placeholder: {c}/{len_data}")
        pl_text = text
        for start, end, label in ents['entities']:
            placeholder = get_placeholder_name_and_surname(end - start).replace('-', ' ')
            pl_text = pl_text[:start] + placeholder + pl_text[end:]
        new_data.append([kgid, text, ents, pl_text])
    return new_data


def test_with_placeholder_common_word(data):
    new_data = []
    c = 0
    len_data = len(data)
    for kgid, text, ents in data:
        c += 1
        print(f"create placeholder: {c}/{len_data}")
        pl_text = text
        for start, end, label in ents['entities']:
            placeholder = get_placeholder_common_name(end - start).replace('-', ' ')
            pl_text = pl_text[:start] + placeholder + pl_text[end:]
        new_data.append([kgid, text, ents, pl_text])
    return new_data
