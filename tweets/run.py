import csv
import tweets.storer as storer


def data():
    tickers = []
    accounts = []
    ticker = 4
    account_twitter = 7

    with open('/home/marco/Scrivania/tirocinio-unicredit/compagnie.tsv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)  # skip header row
        for row in csv_reader:
            if row[ticker] not in tickers:
                tickers.append(row[ticker])
            if row[account_twitter] and row[account_twitter] not in accounts:
                accounts.append(row[account_twitter])
        return tickers, accounts


tickers, accounts = data()
storer.store(tickers, 'hashtag')
storer.store(accounts, 'account')
