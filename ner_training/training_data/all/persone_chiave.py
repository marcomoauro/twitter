def filler_it(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        value = replace_bad_values(row['Value'])
        value = value.split(':')[0].replace('_', ' ').replace('CFO', '')
        if value == '':
            continue

        d.setdefault(row['Resource'].replace('_', ' ').lower(), {'KEY_PEOPLE': []})['KEY_PEOPLE'].append(value)
    return d


def replace_bad_values(value):
    bad_values = ['Board_of_directors', 'Supervisory_board', 'Dr.', 'Dr', 'CFO', 'President', 'president','music industry executive', 'astronomer',
                  'businesswoman', 'engineer', 'Gen. Director', 'CAPT.', '24 Sep 2018', '– MD', 'Prof.', 'founder', '\\',
                  'CEO', 'publisher', 'Director', 'aerospace', 'designer', 'MD', 'CBE', 'Founder', '&', 'group', 'Group', ' co ',
                  ' co', 'co ', ' cto', 'cto ', ' cto ']
    for bv in bad_values:
        value = value.replace(bv, '')
    return value.strip()


def filler_en(infobox_df, key_value):
    d = {}
    for index, row in infobox_df.iterrows():
        if row['Property'] != key_value:
            continue

        value = replace_bad_values(row['Value'])
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
            if ',' in value:
                values = []
                values_splitted = value.split(',')
                for vs in values_splitted:
                    values.append(vs.strip())
            else:
                values = [value.strip()]

        for v in values:
            d.setdefault(row['Resource'].replace('_', ' ').lower(), {'KEY_PEOPLE': []})['KEY_PEOPLE'].append(v)
    return d
