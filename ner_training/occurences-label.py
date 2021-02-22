import json
from operator import itemgetter


def get_space(dim):
    s = ''
    for _ in range(dim, 10):
        s += ' '
    return s


if __name__ == '__main__':
    labels_dict = {'train': {}, 'total_train': 0, 'test': {}, 'total_test': 0}
    train_path = '/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/train.json'
    test_path = '/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/train_placeholder.json'
    for file, kind in [[train_path, 'train'], [test_path, 'test']]:
        parsed_file = json.load(open(file))
        for _, news, occs in parsed_file:
            for start, end, _ in occs['entities']:
                label = news[start:end].lower()
                labels_dict[kind][label] = labels_dict[kind].get(label, 0) + 1
                labels_dict[f"total_{kind}"] += 1

    train_list = sorted(list(labels_dict['train'].items()), key=itemgetter(1), reverse=True)
    test_list = sorted(list(labels_dict['test'].items()), key=itemgetter(1), reverse=True)
    print('=== LABELS ===')
    print()
    print(f"Train: {labels_dict['total_train']}")
    print(f"Test: {labels_dict['total_test']}")
    print()
    print('***** FORMAT: (TRAIN) (TEST)         (LABEL) *****')
    print()
    print('=== LABELS IN TRAIN AND TEST ===')
    for l, occ in train_list:
        if l in labels_dict['test'].keys():
            print(occ, labels_dict['test'][l], get_space(len(f"{occ}{labels_dict['test'][l]}")), l)
    print('\n=== LABELS ONLY IN TRAIN ===')
    for l, occ in train_list:
        if l not in labels_dict['test'].keys():
            print(occ, 0, get_space(len(f"{occ}")), l)

    print('\n=== LABELS ONLY IN TEST ===')
    for l, occ in test_list:
        if l not in labels_dict['train'].keys():
            print(0, occ, get_space(len(f"{occ}")), l)
