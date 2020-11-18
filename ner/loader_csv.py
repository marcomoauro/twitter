import pandas as pd


def load_csv(filename):
    file = open('/home/marco/Scrivania/tirocinio-unicredit/comunicati/aggregati/' + filename)
    return pd.read_csv(file, sep='|')
