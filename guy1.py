import pandas as pd


def getpopulationdf() -> pd.DataFrame:
    return pd.read_csv('Population.csv')

def getgenderdf():
    return pd.read_csv('GenderRatio.csv')

def getpneumodf():
    return pd.read_csv('pneumo.csv')

dfs = [getgenderdf(), getpneumodf(), getpopulationdf()]

for df in dfs:
    print(df.head())
