
# You have to use pip to install the libraries needed to run the program
# Use `pip install -r requirements.txt`
# See the requirements.txt file in the root folder of this repository
from matplotlib import pyplot as plt
from typing import Union, List
import pandas as pd
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn import preprocessing
import logging


logging.getLogger('matplotlib.pyplot').setLevel(logging.WARNING)

ModelRegressor = Union[LinearRegression, LassoCV]


class Model:

    model: ModelRegressor
    in_data: pd.DataFrame
    predictions: pd.Series
    out_data: pd.DataFrame
    in_cols: List[str]
    out_cols: List[str]

    @classmethod
    def normalize(cls, data: pd.DataFrame) -> pd.DataFrame:
        '''
        Function that doesn't change the input. It only returns the input data with all of the values normalized through scaling
        :param data: inputdataframe
        :return: Scaled inputdataframe
        '''
        scaler = preprocessing.MinMaxScaler()
        scaled_input = scaler.fit_transform(data)
        normalized_df = pd.DataFrame(scaled_input)
        return normalized_df

    def __init__(
            self,
            *,
            raw_data: pd.DataFrame,
            in_cols: List[str],
            out_cols: List[str],
            ):
        '''
        :param raw_data: Raw data to input
        :param in_cols: Columns to use as predictors
        :param out_cols: Columns to use to predict
        '''
        self.raw_data = raw_data
        self.out_cols = out_cols
        self.in_cols = in_cols
        self.set_in_data()
        self.set_out_data()

    def set_in_data(self):
        self.in_data = pd.DataFrame(self.raw_data[self.in_cols])

    def set_out_data(self):
        self.out_data = self.raw_data[self.out_cols]

    def set_predictions(self):
        self.predictions = self.model.predict(self.in_data)

    def get_linear_regression(self, reg_in_data, reg_out_data) -> LinearRegression:
        return LinearRegression().fit(reg_in_data, reg_out_data)

    def build_model(self) -> LinearRegression:
        self.model = self.get_linear_regression(self.in_data, self.out_data)
        self.set_predictions()

    def plot(self, input_col: str):
        legend_cols = []
        for i, col in enumerate(self.out_cols):
            plt.plot(self.in_data[input_col], self.out_data[col], 'x')
            legend_cols.append('Actual {}'.format(col))
            plt.plot(self.in_data[input_col], self.predictions[:, i])
            legend_cols.append('Predicted {}'.format(col))
            plt.xlabel(input_col)
            plt.ylabel(col)

        plt.title('{} vs {}'.format(input_col, self.out_cols))
        plt.gca().legend(legend_cols)
        plt.show()
