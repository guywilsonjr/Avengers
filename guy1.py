import pandas as pd


filename = '/home/guy/Downloads/ranks.xlsx'
my_table = pd.read_excel(filename, sheet_name=None)
for page_name, dataset in my_table.items():
    print(dataset)
