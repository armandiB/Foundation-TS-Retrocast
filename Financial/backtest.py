import numpy as np
import pandas as pd

def bbb(index_list, prediction_list, forecasted_data, quantile_for_prediction=0.5):
    index_df = []
    values_df = []
    for index, prediction_dict in zip(index_list, prediction_list):
        first_prediction_point = index[0]
        first_prediction_value = prediction_dict[quantile_for_prediction][0]
        forward_return = forecasted_data[first_prediction_point.date()]
        index_df += [first_prediction_point]
        values_df += [[first_prediction_value, forward_return]]

    pd.DataFrame(values_df, index=index_df, columns=[''])