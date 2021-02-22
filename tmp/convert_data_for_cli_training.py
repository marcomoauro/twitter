import spacy
import srsly
import json
from spacy.gold import docs_to_json, biluo_tags_from_offsets, spans_from_biluo_tags

nlp = spacy.load('en_core_web_lg')
for i in range(114):
    train_data = json.load(open(f"/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/cli/train_placeholder/{i}.json"))

    docs = []
    c = 0
    for kgid, text, annot in train_data:
        c += 1
        print(c)
        doc = nlp(text)
        tags = biluo_tags_from_offsets(doc, annot['entities'])
        entities = spans_from_biluo_tags(doc, tags)
        doc.ents = entities
        docs.append(doc)

    srsly.write_json(f"/home/marco/Scrivania/tirocinio-unicredit/news/final_attempt/training_data/sector/cli/train_placeholder/gold/{i}.json", [docs_to_json(docs)])
