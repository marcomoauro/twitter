import collections


def _entities(nlp, text, filtered_labels=[], threshold=0.8):
    results = []
    with nlp.disable_pipes('ner'):
        doc = nlp(text)

    beams = nlp.entity.beam_parse([doc], beam_width=16, beam_density=0.0001)

    entity_scores = collections.defaultdict(float)
    for beam in beams:
        for score, ents in nlp.entity.moves.get_beam_parses(beam):
            for start, end, label in ents:
                entity_scores[(start, end, label)] += score

    for key in entity_scores:
        start, end, label = key
        score = entity_scores[key]
        if score > threshold:
            if not filtered_labels:
                results.append(result_to_dict(label, doc[start:end], score))
            elif label in filtered_labels:
                results.append(result_to_dict(label, doc[start:end], score))
    return results


def entities(nlp, text, filtered_labels=[], threshold=0.8):
    results = []
    with nlp.disable_pipes('ner'):
        doc = nlp(text)

    beams = nlp.entity.beam_parse([doc], beam_width=16, beam_density=0.0001)

    entity_scores = collections.defaultdict(float)
    for beam in beams:
        for score, ents in nlp.entity.moves.get_beam_parses(beam):
            for start, end, label in ents:
                entity_scores[(start, end, label)] += score

    for key in entity_scores:
        start, end, label = key
        score = entity_scores[key]
        if score > threshold:
            if not filtered_labels:
                results.append(result_to_dict(label, doc[start:end], score))
            elif label in filtered_labels:
                results.append(result_to_dict(label, doc[start:end], score))
    return results

def result_to_dict(label, text, score):
    return(
        {
            'label': label,
            'text': text.text,
            'score': score
        }
    )
