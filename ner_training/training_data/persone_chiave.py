def filler_it(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        value = row['Value'].split(':')[0].replace('_', ' ').replace('CFO', '')
        if value == '':
            continue

        d.setdefault(row['Resource'].lower(), []).append(value)
    return d


def filler_en(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        value = row['Value'].replace('Board_of_directors', '').replace('Supervisory_board', '').replace('Dr.', '').replace('CFO', '').replace('President', '')
        value = value.split(':')[0].replace('_', ' ')
        if value == '':
            continue

        if ' and ' in value or ' and' in value or (len(value) > 2 and value[0:3] == 'and'):
            values_raw = value.split('and')
            values = []
            for v in values_raw:
                vv = v.strip()
                if vv != '':
                    values.append(vv)
        else:
            values = [value]

        for v in values:
            d.setdefault(row['Resource'].lower(), []).append(v)
    return d
