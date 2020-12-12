import pandas as pd


if __name__ == '__main__':
    df=pd.read_csv('/home/marco/Scrivania/tirocinio-unicredit/graphdb/nodes/2020-12-05/tweet_nodes.csv', sep='\t')
    df1 = df[df['isin'].notnull()]
    df2 = df[df['isin'].isnull()]
    df1.to_csv('/home/marco/Scrivania/tirocinio-unicredit/graphdb/neoj4-import-dir/tweet_nodes_company_2020-12-05.csv', index=False, header=True, sep='\t')
    df2.to_csv('/home/marco/Scrivania/tirocinio-unicredit/graphdb/neoj4-import-dir/tweet_nodes_2020-12-05.csv', index=False, header=True, sep='\t')
