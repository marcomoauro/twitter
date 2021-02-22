import re


def filler_it(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        values = row['Value'].replace('_', ' ').replace('\\', "").replace('(California)', "").replace('(Germania)', "").split('n*')
        for value in values:
            if value == '':
                continue
            value = value.replace('*', '').strip()
            d.setdefault(row['Resource'].lower(), []).append(value)
    return d


def filler_en(infobox_df):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != 'hqLocation' and row['Property'] != 'hqLocationCity' and row['Property'] != 'hqLocationCountry':
            continue

        values = str(row['Value']).replace('_', ' ').replace('\\', "").replace('(California)', "").replace('(Germania)', "").split('n*')
        for value in values:
            value = value.replace('*', '').strip()
            if value == '' or value == 'nan' or re.search(r'\d', value):
                continue
            d.setdefault(row['Resource'].lower(), []).append(value)
    return d
