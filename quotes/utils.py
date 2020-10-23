import settings as settings
import csv
import os
import json


def data():
    names = []
    accounts = []
    name = 0
    account_twitter = 7

    with open(settings.COMPANIES_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip header row
        for row in csv_reader:
            if row[name] not in names:
                names.append(row[name])
            if row[account_twitter] and row[account_twitter] not in accounts:
                accounts.append(row[account_twitter])

        return names, accounts


def companies_quotes(text, accounts):
    companies_presents = []
    splitted_text = text.split(' ')
    for account in accounts:
        for word in splitted_text:
            if f"#{account}" == word or f"@{account}" == word:
                companies_presents.append(account)
    return companies_presents


def save_data(tweets_quotes, kind, date):
    directory_path = settings.QUOTES_DATA_FOLDER + f"{date}/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    with open(settings.QUOTES_DATA_FOLDER + f"{date}/{kind}.json", 'w') as outfile:
        json.dump(tweets_quotes, outfile)
