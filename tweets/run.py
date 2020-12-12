import tweets.storer as storer
import tweets.loader as loader
import settings
import datetime


def save_timestamp():
    with open(settings.TIMESTAMP_FILE, 'w') as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))


if __name__ == '__main__':
    tickers, accounts, companies_names, indexes = loader.data()
    #storer.store(tickers, 'hashtag_ticker')
    storer.store(accounts, 'account')
    storer.store(companies_names, 'hashtag_company')
    storer.store(indexes, 'index')
    save_timestamp()
