import csv
import settings

PUNCTUATION = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''


def remove_big_companies(accounts, companies_names):
    accounts.remove('NetflixIT')
    accounts.remove('Apple')
    accounts.remove('AmazonNewsItaly')
    accounts.remove('Facebook')
    companies_names.remove('netflix')
    companies_names.remove('apple')
    companies_names.remove('amazon')
    companies_names.remove('facebook')


def data():
    tickers = []
    accounts = []
    companies_names = []
    ticker = 4
    account_twitter = 7
    name_company = 0

    indexes = ['ftsemib']

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

        remove_big_companies(accounts, companies_names)
        return tickers, accounts, companies_names, indexes
