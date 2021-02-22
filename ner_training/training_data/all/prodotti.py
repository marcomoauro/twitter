import re


def filler_it(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        values = row['Value'].split(':')[0].replace('_', ' ').replace('\\', "").replace('(mass media)', "").split('n*')
        for value in values:
            if value == '':
                continue

            value = value.replace('*', '').strip()
            if '#' in value or '&' in value or re.search(r'\d', value):
                continue

            if ',' in value:
                vals = value.split(',')
                for v in vals:
                    vv = v.strip()
                    d.setdefault(row['Resource'].lower(), []).append(vv)
            else:
                d.setdefault(row['Resource'].lower(), []).append(value)
    return d


def filler_en(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        values = str(row['Value']).split(':')[0].replace('_', ' ').replace('\\', "").replace('(mass media)', "").split('n*')
        for value in values:
            if value == '':
                continue

            value = value.replace('*', '').strip()
            if '#' in value or '&' in value or re.search(r'\d', value) or value == 'nan':
                continue

            if ' and ' in value:
                vals = value.split(' and ')
                for v in vals:
                    vv = v.strip()
                    d.setdefault(row['Resource'].replace('_', ' ').lower(), {'PRODUCT': []})['PRODUCT'].append(vv)

            else:
                d.setdefault(row['Resource'].replace('_', ' ').lower(), {'PRODUCT': []})['PRODUCT'].append(value)

    return d
