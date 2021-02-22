import json
import spacy
from test_set_with_placeholder import test_with_placeholder
from test_set_with_placeholder import test_with_placeholder_name_and_surname
from test_set_with_placeholder import test_with_placeholder_common_word


def get_ground_truths(text, ents):
    gt = []
    for start, end, _ in ents['entities']:
        gt.append(text[start:end].lower())
    return list(set(gt))


def get_real_value(start, end, text, ents, label_text):
    for s, e, _ in ents['entities']:
        if s == start and e == end:
            return text[start:end].lower()
    return label_text


def get_ents_text(doc_ents, text, ents):
    ts = []
    for e in doc_ents:
        start = e.start_char
        end = e.end_char
        real_value = get_real_value(start, end, text, ents, e.text.lower())
        ts.append(real_value)
    return list(set(ts))


if __name__ == '__main__':
    try:
        precisions = []
        recalls = []
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        nlp = spacy.load('/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/model/model-best/')
        evaluation_set = test_with_placeholder_common_word(json.load(open('/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/test.json')))
        c = 0
        len_ev_set = len(evaluation_set)
        for _, text, ents, pl_text in evaluation_set:
            c += 1
            print(f"evaluation: {c}/{len_ev_set}")
            true_positive = 0
            false_positive = 0
            false_negative = 0
            ground_truths = get_ground_truths(text, ents)
            doc = nlp(pl_text)
            doc_ents = get_ents_text(doc.ents, text, ents)
            if len(doc_ents) == 0:
                continue

            for doc_ent in doc_ents:
                if doc_ent in ground_truths:
                    true_positive += 1
                    true_positives += 1
                else:
                    false_positive += 1
                    false_positives += 1
            for gt_ent in ground_truths:
                if gt_ent not in doc_ents:
                    false_negative += 1
                    false_negatives += 1

            precision = true_positive / (true_positive + false_positive)
            recall = true_positive / (true_positive + false_negative)
            precisions.append(precision)
            recalls.append(recall)

        micro_precision = sum(precisions) / len(precisions)  # average of precision of each document
        micro_recall = sum(recalls) / len(recalls)  # average of recall of each document
        micro_f_measure = (2 * micro_precision * micro_recall) / (micro_precision + micro_recall)
        macro_precision = true_positives / (true_positives + false_positives)  # precision consider all like one big document
        macro_recall = true_positives / (true_positives + false_negatives)  # recall consider all like one big document
        macro_f_measure = (2 * macro_precision * macro_recall) / (macro_precision + macro_recall)
        print(f"Micro - Precision: {round(micro_precision * 100, 1)}% - Recall: {round(micro_recall * 100, 1)}% - F1 Measure: {round(micro_f_measure * 100, 1)}%")
        print(f"Macro - Precision: {round(macro_precision * 100, 1)}% - Recall: {round(macro_recall * 100, 1)}% - F1 Measure: {round(macro_f_measure * 100, 1)}%")
    except ZeroDivisionError as e:
        print()
