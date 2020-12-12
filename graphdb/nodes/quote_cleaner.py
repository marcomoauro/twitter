import pandas as pd


if __name__ == '__main__':
    path = '/home/marco/Scrivania/tirocinio-unicredit/graphdb/neoj4-import-dir/tweet_2020-12-05/tweet_nodes.csv'
    df = pd.read_csv(path, sep='\t')
    df['text'] = df['text'].apply(lambda t: str(t).replace('\"', ' '))
    df.to_csv(path, index=False, header=True, sep ='\t')
