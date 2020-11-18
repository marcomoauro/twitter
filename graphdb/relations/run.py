import graphdb.relations.labeler as labeler
import graphdb.relations.temp_storer as temp_storer
import graphdb.relations.storer as storer
import spacy
from spacy_cld import LanguageDetector


def temp_relations(file, nlp_detect, nlps):
    file_type = temp_relations_file_type(file)
    label_dict = labeler.create_label_dict(file, nlp_detect, nlps, file_type)
    temp_storer.store(file_type, label_dict)


def temp_relations_file_type(file):
    return file.split('/')[-1].split('_nodes')[0]


def relations_file_type(file):
    return '_'.join(file.split('/')[-1].split('_')[1:-1])


def relations(file):
    storer.store(relations_file_type(file), file)


def oldest_timestamp():
    f = open('/home/marco/Scrivania/tirocinio-unicredit/graphdb/timestamp.txt', 'r')
    return f.read().strip()


def nodes_files():
    base_path = '/home/marco/Scrivania/tirocinio-unicredit/graphdb/nodes/'
    #return [base_path + oldest_timestamp() + '/tweet_nodes.csv']#, base_path + 'com_stampa_nodes.csv']
    return [base_path + 'com_stampa_nodes.csv']#,base_path + oldest_timestamp() + '/tweet_nodes.csv']


def relations_files():
    base_path = '/home/marco/Scrivania/tirocinio-unicredit/graphdb/relations/'
    #return [base_path + oldest_timestamp() + '/tweet_nodes.csv', base_path + 'com_stampa_nodes.csv']
    return [base_path + '2020-11-14' + '/temp_tweet_relations.csv', base_path + 'temp_com_stampa_relations.csv']


def init_nlp():
    nlp_detect = spacy.load('en_core_web_lg')
    nlp_detect.add_pipe(LanguageDetector())

    nlps = {
        'it': spacy.load('it_core_news_lg'),
        'en': spacy.load('en_core_web_lg')
    }
    return nlp_detect, nlps


if __name__ == '__main__':
    # =======================
    action = 'build_temp_relation'  # [build_temp_relation, build_relation]
    # =======================

    if action == 'build_temp_relation':
        nlp_detect, nlps = init_nlp()

        for file in nodes_files():
            temp_relations(file, nlp_detect, nlps)

    if action == 'build_relation':
        for file in relations_files():
            relations(file)
