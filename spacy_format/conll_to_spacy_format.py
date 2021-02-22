import json
from spacy_format.emerging_to_spacy_format import add_with_spacy_format


def finish_doc(line):
    return line == '-DOCSTART- -X- O O'


if __name__ == '__main__':
    file = open('/home/marco/Scrivania/conll/eng.testa', 'r')
    lines = file.readlines()
    spacy_docs = []
    ss = []
    l = ''
    prec = False
    for line in lines:
        line = line.strip()
        if finish_doc(line):
            s = ' '.join(ss)
            s += ' '
            l = l.strip()[1:]
            if l != '':
                add_with_spacy_format(spacy_docs, s, l, 'PERSON')
            ss = []
            l = ''
            prec = False
        else:
            if line == '':
                continue

            word, _, _, label = line.split(' ')

            ss.append(word)
            if label == 'I-PER':
                if prec:
                    l += ' ' + word
                else:
                    l += '|'
                    l += word
                prec = True
            else:
                prec = False
    with open(f"/home/marco/Scrivania/conll_files/person/test_a.json", 'w') as outfile:
        json.dump(spacy_docs, outfile)
