import csv
import tweets.storer as storer
import settings
import datetime

INDEXES_QUERY = ['ftsemib']

def data():
    tickers = []
    accounts = []
    indexes = []
    ticker = 4
    account_twitter = 7
    index = 6

    with open(settings.COMPANIES_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip header row
        for row in csv_reader:
            if row[ticker] not in tickers:
                tickers.append(row[ticker])
            if row[account_twitter] and row[account_twitter] not in accounts:
                accounts.append(row[account_twitter])
            if row[index] and row[index] not in indexes:
                indexes.append(row[index])

        return tickers, accounts, indexes


def save_timestamp():
    with open(settings.TIMESTAMP_FILE, 'w') as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))


if __name__ == '__main__':
    tickers, accounts, indexes = data()
    storer.store(tickers, 'hashtag')
    storer.store(accounts, 'account')
    storer.store(INDEXES_QUERY, 'index')
    save_timestamp()
