import json
import spacy


def get_ground_truths(text, ents):
    gt = []
    for start, end, _ in ents['entities']:
        gt.append(text[start:end].lower())
    return list(set(gt))


if __name__ == '__main__':
    try:
        precisions = []
        recalls = []
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        nlp = spacy.load('/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/model/model-best/')
        evaluation_set = json.load(open('/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/test.json'))
        len_ev_set = len(evaluation_set)
        c=0
        for _, text, ents in evaluation_set:
            c += 1
            print(f"{c}/{len_ev_set}")
            true_positive = 0
            false_positive = 0
            false_negative = 0
            ground_truths = get_ground_truths(text, ents)
            doc = nlp(text)
            doc_ents = list(set(map(lambda e: e.text.lower(), doc.ents)))
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
