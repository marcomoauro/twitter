def calculate_common_orgs():
    file = open('/home/marco/Scrivania/tirocinio-unicredit/common/gdelt-organization-by-frequency.txt', 'r')
    lines = file.readlines()
    common_orgs = []
    for line in lines:
        splitted_line = line.replace("\n", '').split(' ')
        occ = splitted_line[0]
        words = splitted_line[1:]
        if int(occ) < 10:
            break
        common_orgs.append(' '.join(words).lower())
    return common_orgs


COMMON_ORGANIZATIONS = calculate_common_orgs()
