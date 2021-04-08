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


def run():
    # Change the filename to whatever you want
    filename = 'us.csv'
    data = pd.read_csv(filename)
    data = add_daynumber(data)
    mymodel = model.Model(raw_data=data, in_cols=['daynumber'], out_cols=['cases', 'deaths'])
    mymodel.build_model()
    mymodel.plot('daynumber')

run()