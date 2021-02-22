import pandas as pd
import os


if __name__ == '__main__':
    df = pd.read_csv('/home/marco/Scrivania/tirocinio-unicredit/news/all/kgid_company.csv', sep='|')
    for index, row in df.iterrows():
        isin_file_path = f"/home/marco/Scrivania/tirocinio-unicredit/news/all/kgid_by_company/{row['company']}.csv"
        if not os.path.exists(isin_file_path):
            with open(isin_file_path, "a") as isin_file:
                print('kgid', file=isin_file)
                isin_file.close()
        with open(isin_file_path, "a") as isin_file:
            print(index)
            print(row['kgid'], file=isin_file)
