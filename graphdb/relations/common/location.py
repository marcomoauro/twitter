def calculate_common_locations():
    file = open('/home/marco/Scrivania/tirocinio-unicredit/common/gdelt-location-by-frequency.txt', 'r')
    lines = file.readlines()
    common_locations = []
    for line in lines:
        splitted_line = line.replace("\n", '').split(' ')
        occ = splitted_line[0]
        name = splitted_line[1].split('#')[1].lower()
        if int(occ) < 10:
            break
        common_locations.append(name)
    return common_locations


COMMON_LOCATIONS = calculate_common_locations()
