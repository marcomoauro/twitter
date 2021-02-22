import os
import settings
import pandas as pd


def get_isin_to_company():
    d = {}
    df = pd.read_csv(settings.COMPANIES_FILE_PATH)
    for index, row in df.iterrows():
        d[row['ISIN']] = row['Nome'].lower()
    return d


if __name__ == '__main__':
    companies = ['a2a', 'axa', 'datalogic', 'amgen', 'webuild', 'nokia', 'nexi', 'danieli', 'iberdrola', 'peugeot', 'snam',
     'airbus', 'heidelbergcement', 'italgas', 'eni', 'mediaset', 'safran', 'unilever', 'telefonica', 'mediobanca',
     'carrefour', 'siemens', 'technogym', 'kering', "l'oréal", 'sanofi', 'moncler', 'allianz', 'bayer', 'netflix',
     'heidelberg_cement', 'repsol', 'avio', 'autogrill', 'geox', 'amplifon', 'adidas', 'unieuro', 'unicredit',
     'anheuser-busch', 'pirelli', 'inditex', 'unipol', 'enel', 'intel', 'brembo', 'thyssenkrupp', 'vonovia', 'inwit',
     'elica', 'beiersdorf', 'lufthansa', 'piaggio', 'enav', 'fincantieri', 'tripadvisor', 'diasorin', 'philips',
     'vivendi', 'ageas', 'nokia_corporation', 'saipem', 'volkswagen', 'ferrari', 'emak', 'stmicroelectronics', 'basf',
     'tiscali', "l'oreal", 'danone', 'citigroup', 'piquadro', 'commerzbank', 'renault', 'engie', 'bmw', 'tenaris',
     'deutsche_lufthansa', 'telefónica', 'astaldi']
    isin_to_company = get_isin_to_company()
    directory = '/home/marco/Scrivania/tirocinio-unicredit/news/news_by_isin_to_label'
    for filename in os.listdir(directory):
        isin = filename.split('.')[0]
        if isin_to_company.get(isin, '___') not in companies:
            os.remove(directory + '/' + filename)

