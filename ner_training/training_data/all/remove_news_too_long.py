import json


train = json.load(open(f"/home/marco/Scrivania/tirocinio-unicredit/news/all/training_data/en-sector/subset/test.json"))
new_train = []
c=0
for t in train:
    if len(t[0]) > 50000:
        c+=1
        print(c)
    else:
        new_train.append(t)
with open('/home/marco/Scrivania/tirocinio-unicredit/news/all/training_data/en-keypeople/data_short.json', 'w') as f:
    json.dump(new_train, f)
