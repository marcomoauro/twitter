import csv
import tweets.storer as storer
import settings
import datetime

INDEXES_QUERY = ['ftsemib']
PUNCTUATION = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''

def data():
    tickers = []
    accounts = []
    companies_names = []
    ticker = 4
    account_twitter = 7
    name_company = 0

    with open(settings.COMPANIES_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip header row
        for row in csv_reader:
            if row[ticker] not in tickers:
                tickers.append(row[ticker])
            if row[account_twitter] and row[account_twitter] not in accounts:
                accounts.append(row[account_twitter])

            name = row[name_company]
            for c in name:
                if c in PUNCTUATION:
                    name = name.replace(c, '')
            name = name.lower()
            if name not in companies_names:
                companies_names.append(name)

        return tickers, accounts, companies_names


def save_timestamp():
    with open(settings.TIMESTAMP_FILE, 'w') as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))


if __name__ == '__main__':
    tickers, accounts, companies_names = data()
    #storer.store(tickers, 'hashtag_ticker')
    storer.store(accounts, 'account')
    storer.store(companies_names, 'hashtag_company')
    storer.store(INDEXES_QUERY, 'index')
    save_timestamp()
