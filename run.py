import pandas as pd
import numpy as np
import model


def add_daynumber(raw_data: pd.DataFrame, startswith=0):
    '''
    adds a daynumber column starting from zero because 01/01/2020 is not a number
    '''
    data_copy = raw_data.copy()
    data_copy['daynumber'] = np.arange(data_copy.shape[0]) + startswith
    return data_copy

def add_columnfromdf1todf2(column_name: str, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    '''
    Get a new data frame where if the call is add_columnsfromdf1todf2(col2, df1, df2)
    df1:
        col1 col2
    al    a   b
    ca    c   d
    and df2:
        col3 col4
    al   1    2
    ca   3    4

    returns a new df2:
        col3 col4 col2
    al   1    2   b
    ca   3    4   d
    '''
    df2[column_name] = df1[column_name]
    return df2

def run():
    # Change the filename to whatever you want
    filename = 'us.csv'
    data = pd.read_csv(filename)
    data = add_daynumber(data)
    mymodel = model.Model(raw_data=data, in_cols=['daynumber'], out_cols=['cases', 'deaths'])
    mymodel.build_model()
    mymodel.plot('daynumber')

run()
