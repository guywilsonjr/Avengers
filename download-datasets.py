import requests

datasetnames = {
    'Invasive pneumococcal disease': 'table1s'
}
def getdataforweek(datasetname: str, year: int, weeknumber: int):
    urlformat = f'https://wonder.cdc.gov/nndss/static/{year}/{weeknumber}/{year}-{weeknumber}-{datasetname}.html'
    print(urlformat)
    data = requests.get(urlformat)
    print(data.content)
    return

def getdataforyear(year: int, datasetname: str):
    datasets = []
    for i in range(1):
        week = '%02d' % (i+1)
        datasets.append(getdataforweek(datasetname, year, week))
    return datasets

def download_data():
    for key, data in datasetnames.items():
        getdataforyear(2020, data)

download_data()
