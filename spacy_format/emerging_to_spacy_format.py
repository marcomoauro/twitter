import json
KEY_LABEL = 'LOCATION'
CONLL_LABEL = 'location'


def is_overlapped(new_pos, start, end):
    xs = set(range(start, end))
    for act_start, act_end, act_label in new_pos:
        y = range(act_start, act_end)
        if len(xs.intersection(y)) > 0:
            return True
    return False


def remove_overlapped(positions):
    new_pos = []
    for start, end, label in positions:
        if is_overlapped(new_pos, start, end):
            continue
        new_pos.append((start, end, label))
    return new_pos


def remove_duplicates(positions):
    dups = []
    filtered_positions = []
    for start, end, key_label in positions:
        key_string = f"{start}_{end}_{key_label}"
        if key_string not in dups:
            filtered_positions.append((start, end, key_label))
            dups.append(key_string)
    return filtered_positions


def asterics_string(label_length):
    s = ''
    for i in range(label_length):
        s += '*'
    return s


def get_positions(labels, text_parsed, key_label):
    positions = []
    for label in labels:
        label_length = len(label)
        index = 0
        while index < len(text_parsed):
            index = text_parsed.find(label, index)
            if index == -1:
                break
            if text_parsed[index - 1] == ' ' and text_parsed[index + label_length] == ' ':
                positions.append((index, index + label_length, key_label))
                text_parsed = text_parsed.replace(label, asterics_string(label_length), 1)
            index += label_length
    positions = remove_duplicates(positions)
    positions = remove_overlapped(positions)
    return positions


def is_finish_doc(splitted_line):
    return splitted_line == ['']


def add_with_spacy_format(docs, text, labels, key_label):
    positions = get_positions(labels.split('|'), text, key_label)
    if positions == []:
        return

    docs.append((text, {'entities': positions}))


if __name__ == '__main__':
    file = open('/home/marco/Scrivania/emerging_entities_17/test.annotated', 'r')
    lines = file.readlines()
    spacy_docs = []
    ss = []
    l = ''
    for line in lines:
        line = line.strip()
        splitted_line = line.split('\t')
        if is_finish_doc(splitted_line):
            s = ' '.join(ss)
            s += ' '
            #s = s.replace(" '", "'").replace(" .", ".")
            l = l.strip()[1:]
            if l != '':
                add_with_spacy_format(spacy_docs, s, l, KEY_LABEL)
            ss = []
            l = ''
        else:
            stringa, labels = splitted_line
            ss.append(stringa)
            if labels == f"B-{CONLL_LABEL}":
                l += '|'
                l += stringa
            if labels == f"I-{CONLL_LABEL}":
                l += ' ' + stringa
    with open(f"/home/marco/Scrivania/emerging_entities_files/{KEY_LABEL.lower()}/test.json", 'w') as outfile:
        json.dump(spacy_docs, outfile)
