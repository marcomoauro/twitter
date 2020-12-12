import pandas as pd


def node_file():
    return '/home/marco/Scrivania/tirocinio-unicredit/graphdb/neoj4-import-dir/tweet_2020-12-05/tweet_nodes_2020-12-05.csv'


def filtered_node_file():
    node_file_path_splitted = node_file().split('.csv')
    return f"{node_file_path_splitted[0]}_filt.csv"


def relations_files():
    base_path = '/home/marco/Scrivania/tirocinio-unicredit/graphdb/relations/2020-12-05/'
    return [
        base_path + 'tweet_PERSON_relations.csv',
        base_path + 'tweet_ORG_relations.csv',
        base_path + 'tweet_GPE_relations.csv'
    ]


if __name__ == '__main__':
    df_node = pd.read_csv(node_file(), sep='\t')
    before = len(df_node.index)
    node_ids = []
    for relation_file in relations_files():
        df_relation = pd.read_csv(relation_file, sep='\t')
        node_ids += list(df_relation['node_id'])
    node_ids = list(set(node_ids))
    for index, row in df_node.iterrows():
        print(index)
        if row['id'] not in node_ids:
            df_node.drop(index, inplace=True)
    print(f"before: {before}")
    print(f"after: {len(df_node.index)}")
    df_node.to_csv(filtered_node_file(), index=False, header=True, sep='\t')
