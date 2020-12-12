def calculate_common_persons():
    file = open('/home/marco/Scrivania/tirocinio-unicredit/common/gdelt-person-by-frequency.txt', 'r')
    lines = file.readlines()
    common_persons = []
    for line in lines:
        splitted_line = line.replace("\n", '').split(' ')
        occ = splitted_line[0]
        words = splitted_line[1:]
        if int(occ) < 10:
            break
        for word in words:
            common_persons.append(word.lower())
    return common_persons


COMMON_NAMES_AND_SURNAMES = calculate_common_persons()
