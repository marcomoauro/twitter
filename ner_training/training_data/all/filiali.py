import re


def filler_it(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        values = row['Value'].replace('\\', "").replace('(azienda)', "").split('n*')
        for value in values:
            value = value.replace('*', '').replace('_', ' ').strip()
            if '#' in value or '&' in value or re.search(r'\d', value):
                continue

            d.setdefault(row['Resource'].lower(), []).append(value)
    return d


def filler_en(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        value = str(row['Value']).replace('_', " ").replace('\\', "").replace('(company)', "")
        value = value.replace('(clothing)', '').replace('(Hong Kong)', '').replace('(Inditex)', '').replace('(telecommunications)', '')
        values = value.split('n*')
        for value in values:
            if '#' in value or '&' in value or re.search(r'\d', value) or value == 'nan' or value == '*' or value == '':
                continue
            value = value.replace('*', '').strip()
            d.setdefault(row['Resource'].replace('_', ' ').lower(), {'SUBSID': []})['SUBSID'].append(value)

    return d
