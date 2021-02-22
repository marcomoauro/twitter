import csv
import sys

csv.field_size_limit(sys.maxsize)


f = 0
c = 0
with open('/home/marco/Scrivania/tirocinio-unicredit/news/news_with_lang.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    next(csv_reader)  # skip header row
    for row in csv_reader:
        f += 1
        print(f)
        if len(row) > 2:
            c += 1
            print(f"------ {c} -------")
